from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .agent import run_investigation, tool_draft_application, tool_track_deadline
from .db import get_db, init_db
from .seed import seed

app = FastAPI(title="ChanceBD", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"


class ProfileCreate(BaseModel):
    name: str = "Student"
    hsc_gpa: float = Field(..., ge=0, le=5)
    hsc_board: str = "Dhaka"
    hsc_group: str = "Science"
    hsc_year: int = 2024
    ssc_gpa: float = Field(..., ge=0, le=5)
    ssc_board: str = "Dhaka"
    ssc_group: str = "Science"
    ssc_year: int = 2022
    preferred_location: str | None = None
    preferred_degree_level: str | None = None


class InvestigateRequest(BaseModel):
    profile_id: int
    program_ids: list[str] | None = None


@app.on_event("startup")
def startup():
    init_db()
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM programs").fetchone()[0]
    conn.close()
    if count == 0:
        seed()


@app.get("/api/health")
def health():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM programs").fetchone()[0]
    conn.close()
    return {"status": "ok", "programs": count}


@app.get("/api/programs")
def list_programs():
    conn = get_db()
    rows = conn.execute("SELECT * FROM programs ORDER BY university, program_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/api/profile")
def create_profile(profile: ProfileCreate):
    conn = get_db()
    cur = conn.execute(
        """INSERT INTO student_profiles (name, hsc_gpa, hsc_board, hsc_group, hsc_year,
           ssc_gpa, ssc_board, ssc_group, ssc_year, preferred_location, preferred_degree_level)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            profile.name,
            profile.hsc_gpa,
            profile.hsc_board,
            profile.hsc_group,
            profile.hsc_year,
            profile.ssc_gpa,
            profile.ssc_board,
            profile.ssc_group,
            profile.ssc_year,
            profile.preferred_location,
            profile.preferred_degree_level,
        ),
    )
    profile_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"profile_id": profile_id, "profile": profile.dict()}


@app.post("/api/investigate")
def investigate(req: InvestigateRequest):
    conn = get_db()
    row = conn.execute("SELECT * FROM student_profiles WHERE id = ?", (req.profile_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile = dict(row)
    result = run_investigation(profile, req.program_ids)

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO investigations (profile_id, status) VALUES (?, ?)",
        (req.profile_id, "completed"),
    )
    inv_id = cur.lastrowid
    for i, step in enumerate(result["steps"]):
        conn.execute(
            "INSERT INTO investigation_steps (investigation_id, tool_name, tool_input, tool_output, step_order) VALUES (?,?,?,?,?)",
            (inv_id, step["tool"], str(step["input"]), str(step["output"]), i),
        )
    for m in result["matches"]:
        conn.execute(
            "INSERT INTO matches (investigation_id, program_id, eligible, fit_score, reasons, deadline_status, days_remaining) VALUES (?,?,?,?,?,?,?)",
            (inv_id, m["program_id"], 0, m["fit_score"], str(m["reasons"]), "", 0),
        )
    for d in result["drafts"]:
        conn.execute(
            "INSERT INTO drafts (investigation_id, program_id, draft_text) VALUES (?,?,?)",
            (inv_id, d["program_id"], d["draft_text"]),
        )
    conn.commit()
    conn.close()

    result["investigation_id"] = inv_id
    return result


@app.get("/api/investigations")
def list_investigations():
    conn = get_db()
    rows = conn.execute("SELECT * FROM investigations ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/investigations/{inv_id}")
def get_investigation(inv_id: int):
    conn = get_db()
    inv = conn.execute("SELECT * FROM investigations WHERE id = ?", (inv_id,)).fetchone()
    if not inv:
        conn.close()
        raise HTTPException(status_code=404, detail="Investigation not found")
    steps = conn.execute(
        "SELECT * FROM investigation_steps WHERE investigation_id = ? ORDER BY step_order", (inv_id,)
    ).fetchall()
    drafts = conn.execute(
        "SELECT * FROM drafts WHERE investigation_id = ?", (inv_id,)
    ).fetchall()
    conn.close()
    return {
        "investigation": dict(inv),
        "steps": [dict(s) for s in steps],
        "drafts": [dict(d) for d in drafts],
    }


@app.get("/api/deadline/{program_id}")
def deadline(program_id: str):
    return tool_track_deadline(program_id)


@app.post("/api/draft/{program_id}")
def draft(program_id: str, profile: dict):
    return tool_draft_application(program_id, profile)


# Serve frontend
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/")
    def index():
        return FileResponse(FRONTEND_DIST / "index.html")

    @app.get("/{path:path}")
    def spa(path: str):
        f = FRONTEND_DIST / path
        if f.exists() and f.is_file():
            return FileResponse(f)
        return FileResponse(FRONTEND_DIST / "index.html")
