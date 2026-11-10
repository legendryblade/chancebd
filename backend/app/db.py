import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "chancebd.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS programs (
            id TEXT PRIMARY KEY,
            university TEXT NOT NULL,
            program_name TEXT NOT NULL,
            degree_level TEXT NOT NULL,
            required_group TEXT,
            min_hsc_gpa REAL,
            min_ssc_gpa REAL,
            min_hsc_gpa_science REAL,
            min_hsc_gpa_humanities REAL,
            min_hsc_gpa_business REAL,
            application_start TEXT,
            application_deadline TEXT,
            exam_date TEXT,
            total_seats INTEGER,
            tuition_fee_bdt INTEGER,
            location TEXT,
            campus TEXT,
            required_documents TEXT,
            notes TEXT,
            official_website TEXT
        );

        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            hsc_gpa REAL,
            hsc_board TEXT,
            hsc_group TEXT,
            hsc_year INTEGER,
            ssc_gpa REAL,
            ssc_board TEXT,
            ssc_group TEXT,
            ssc_year INTEGER,
            preferred_location TEXT,
            preferred_degree_level TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            status TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES student_profiles (id)
        );

        CREATE TABLE IF NOT EXISTS investigation_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investigation_id INTEGER,
            tool_name TEXT,
            tool_input TEXT,
            tool_output TEXT,
            step_order INTEGER,
            FOREIGN KEY (investigation_id) REFERENCES investigations (id)
        );

        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investigation_id INTEGER,
            program_id TEXT,
            eligible INTEGER,
            fit_score REAL,
            reasons TEXT,
            deadline_status TEXT,
            days_remaining INTEGER,
            FOREIGN KEY (investigation_id) REFERENCES investigations (id),
            FOREIGN KEY (program_id) REFERENCES programs (id)
        );

        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investigation_id INTEGER,
            program_id TEXT,
            draft_text TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (investigation_id) REFERENCES investigations (id),
            FOREIGN KEY (program_id) REFERENCES programs (id)
        );
        """
    )
    conn.commit()
    conn.close()
