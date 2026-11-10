import json
from datetime import date, datetime
from typing import Any

from .db import get_db


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def _today() -> date:
    return date.today()


def _fit_score(program: dict, profile: dict) -> float:
    score = 0.0
    reasons = []

    hsc = profile["hsc_gpa"]
    ssc = profile["ssc_gpa"]
    group = profile["hsc_group"]
    min_hsc = program.get("min_hsc_gpa") or 0
    min_ssc = program.get("min_ssc_gpa") or 0

    if hsc >= min_hsc:
        score += 40
        reasons.append(f"HSC GPA {hsc} meets minimum {min_hsc}")
    else:
        reasons.append(f"HSC GPA {hsc} below minimum {min_hsc}")

    if ssc >= min_ssc:
        score += 20
        reasons.append(f"SSC GPA {ssc} meets minimum {min_ssc}")
    else:
        reasons.append(f"SSC GPA {ssc} below minimum {min_ssc}")

    if program.get("required_group"):
        if group == program["required_group"]:
            score += 25
            reasons.append(f"Group {group} matches required {program['required_group']}")
        else:
            reasons.append(f"Group {group} does not match required {program['required_group']}")
    else:
        score += 25
        reasons.append("Open to all groups")

    if profile.get("preferred_location"):
        if profile["preferred_location"].lower() in (program.get("location") or "").lower():
            score += 10
            reasons.append(f"Location {program['location']} matches preference")
        else:
            reasons.append(f"Location {program['location']} differs from preference")

    if profile.get("preferred_degree_level"):
        if profile["preferred_degree_level"] == program["degree_level"]:
            score += 5
            reasons.append(f"Degree level {program['degree_level']} matches preference")

    return min(score, 100), reasons


def _eligible(program: dict, profile: dict) -> tuple[bool, list[str]]:
    reasons = []
    eligible = True

    group = profile["hsc_group"]
    req_group = program.get("required_group")

    if req_group and group != req_group:
        eligible = False
        reasons.append(f"Requires {req_group} group, you have {group}")

    min_hsc = program.get("min_hsc_gpa")
    if min_hsc and profile["hsc_gpa"] < min_hsc:
        eligible = False
        reasons.append(f"HSC GPA {profile['hsc_gpa']} below required {min_hsc}")

    min_ssc = program.get("min_ssc_gpa")
    if min_ssc and profile["ssc_gpa"] < min_ssc:
        eligible = False
        reasons.append(f"SSC GPA {profile['ssc_gpa']} below required {min_ssc}")

    return eligible, reasons


def _deadline_status(deadline_str: str) -> tuple[str, int]:
    deadline = _parse_date(deadline_str)
    days = (deadline - _today()).days
    if days < 0:
        return "closed", days
    if days <= 7:
        return "urgent", days
    if days <= 30:
        return "approaching", days
    return "open", days


def tool_match_programs(profile: dict) -> dict:
    conn = get_db()
    rows = conn.execute("SELECT * FROM programs").fetchall()
    conn.close()

    programs = [dict(r) for r in rows]
    results = []
    for p in programs:
        score, reasons = _fit_score(p, profile)
        results.append(
            {
                "program_id": p["id"],
                "university": p["university"],
                "program_name": p["program_name"],
                "degree_level": p["degree_level"],
                "location": p["location"],
                "tuition_fee_bdt": p["tuition_fee_bdt"],
                "total_seats": p["total_seats"],
                "fit_score": score,
                "reasons": reasons,
            }
        )
    results.sort(key=lambda x: x["fit_score"], reverse=True)
    return {"count": len(results), "matches": results[:20]}


def tool_check_eligibility(program_id: str, profile: dict) -> dict:
    conn = get_db()
    row = conn.execute("SELECT * FROM programs WHERE id = ?", (program_id,)).fetchone()
    conn.close()
    if not row:
        return {"error": f"Program {program_id} not found"}

    p = dict(row)
    eligible, reasons = _eligible(p, profile)
    return {
        "program_id": program_id,
        "university": p["university"],
        "program_name": p["program_name"],
        "eligible": eligible,
        "reasons": reasons,
        "required_group": p.get("required_group"),
        "min_hsc_gpa": p.get("min_hsc_gpa"),
        "min_ssc_gpa": p.get("min_ssc_gpa"),
    }


def tool_track_deadline(program_id: str) -> dict:
    conn = get_db()
    row = conn.execute("SELECT * FROM programs WHERE id = ?", (program_id,)).fetchone()
    conn.close()
    if not row:
        return {"error": f"Program {program_id} not found"}

    p = dict(row)
    status, days = _deadline_status(p["application_deadline"])
    return {
        "program_id": program_id,
        "university": p["university"],
        "program_name": p["program_name"],
        "application_start": p["application_start"],
        "application_deadline": p["application_deadline"],
        "exam_date": p["exam_date"],
        "status": status,
        "days_remaining": days,
    }


def tool_draft_application(program_id: str, profile: dict) -> dict:
    conn = get_db()
    row = conn.execute("SELECT * FROM programs WHERE id = ?", (program_id,)).fetchone()
    conn.close()
    if not row:
        return {"error": f"Program {program_id} not found"}

    p = dict(row)
    docs = json.loads(p["required_documents"] or "[]")
    name = profile.get("name") or "[Your Full Name]"

    draft = f"""APPLICATION DRAFT
{'=' * 60}

To,
The Admission Office
{p['university']}
{p['campus']}, {p['location']}

Subject: Application for {p['program_name']} ({p['degree_level']})

Dear Sir/Madam,

I, {name}, hereby apply for admission to the {p['program_name']} program
at {p['university']} for the academic year 2026-27.

ACADEMIC BACKGROUND
-------------------
HSC: GPA {profile['hsc_gpa']} ({profile['hsc_group']}, {profile['hsc_board']} Board, {profile['hsc_year']})
SSC: GPA {profile['ssc_gpa']} ({profile['ssc_group']}, {profile['ssc_board']} Board, {profile['ssc_year']})

PROGRAM CHOICE
--------------
Program: {p['program_name']}
Degree Level: {p['degree_level']}
Required Group: {p.get('required_group') or 'Any'}
Total Seats: {p['total_seats']}
Tuition Fee: BDT {p['tuition_fee_bdt']:,}

REQUIRED DOCUMENTS
------------------
{chr(10).join(f'{i+1}. {d}' for i, d in enumerate(docs))}

NOTES
-----
{p.get('notes') or ''}

I confirm that the information provided above is true and accurate to the
best of my knowledge. I understand that any false information may result in
the cancellation of my application.

Yours sincerely,
{name}
Date: {_today().strftime('%B %d, %Y')}

{'=' * 60}
Generated by ChanceBD Agent on {_today().strftime('%Y-%m-%d')}
This is a DRAFT. Review all details before submission.
Official website: {p.get('official_website') or 'N/A'}
"""
    return {
        "program_id": program_id,
        "university": p["university"],
        "program_name": p["program_name"],
        "draft_text": draft,
        "required_documents": docs,
    }


TOOLS = {
    "match_programs": tool_match_programs,
    "check_eligibility": tool_check_eligibility,
    "track_deadline": tool_track_deadline,
    "draft_application": tool_draft_application,
}


def run_investigation(profile: dict, selected_program_ids: list[str] | None = None) -> dict:
    """Bounded agent loop: match -> check -> track -> draft for selected programs."""
    steps = []

    match_result = tool_match_programs(profile)
    steps.append(
        {
            "tool": "match_programs",
            "input": {"hsc_gpa": profile["hsc_gpa"], "group": profile["hsc_group"]},
            "output": match_result,
        }
    )

    targets = selected_program_ids or [m["program_id"] for m in match_result["matches"][:3]]
    if not targets:
        targets = [m["program_id"] for m in match_result["matches"][:3]]

    checks = []
    for pid in targets:
        checks.append(tool_check_eligibility(pid, profile))
    steps.append(
        {
            "tool": "check_eligibility",
            "input": {"program_ids": targets},
            "output": checks,
        }
    )

    deadlines = []
    for pid in targets:
        deadlines.append(tool_track_deadline(pid))
    steps.append(
        {
            "tool": "track_deadline",
            "input": {"program_ids": targets},
            "output": deadlines,
        }
    )

    drafts = []
    for pid in targets:
        drafts.append(tool_draft_application(pid, profile))
    steps.append(
        {
            "tool": "draft_application",
            "input": {"program_ids": targets},
            "output": drafts,
        }
    )

    return {
        "profile": profile,
        "matches": match_result["matches"],
        "eligibility": checks,
        "deadlines": deadlines,
        "drafts": drafts,
        "steps": steps,
        "mode": "deterministic",
    }
