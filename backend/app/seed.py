import json
from datetime import date
from pathlib import Path

PROGRAMS = [
    # DU - University of Dhaka
    ("DU-CSE-SCI", "University of Dhaka", "BSc in Computer Science and Engineering", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2026-11-12", "2026-11-18", "2026-12-10", 120, 85000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos","admit card fee"]', "Requires HSC science with physics and math.", "https://du.ac.bd"),
    ("DU-EEE-SCI", "University of Dhaka", "BSc in Electrical and Electronic Engineering", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2026-11-10", "2026-11-14", "2026-12-05", 80, 85000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science with physics, math, chemistry.", "https://du.ac.bd"),
    ("DU-ENG-HUM", "University of Dhaka", "BA in English", "HSC", "Humanities", 3.00, 3.00, None, 3.00, None, "2027-06-10", "2027-07-10", "2027-08-10", 200, 45000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://du.ac.bd"),
    ("DU-BBA-BUS", "University of Dhaka", "BBA in Accounting and Information Systems", "HSC", "Business", 3.00, 3.00, None, None, 3.00, "2027-06-12", "2027-07-12", "2027-08-12", 150, 65000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Commerce background preferred.", "https://du.ac.bd"),
    ("DU-LAW-HUM", "University of Dhaka", "LLB (Honours)", "HSC", "Humanities", 3.25, 3.25, None, 3.25, None, "2027-06-20", "2027-07-20", "2027-08-20", 100, 55000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos","character certificate"]', "Admission test mandatory.", "https://du.ac.bd"),
    ("DU-PHARM-SCI", "University of Dhaka", "BPharm", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2027-06-18", "2027-07-18", "2027-08-18", 60, 75000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://du.ac.bd"),
    ("DU-ECON-SCI", "University of Dhaka", "BSc in Economics", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-14", "2027-07-14", "2027-08-14", 90, 60000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Science or business both accepted.", "https://du.ac.bd"),
    ("DU-JOUR-HUM", "University of Dhaka", "BA in Journalism and Mass Communication", "HSC", "Humanities", 3.00, 3.00, None, 3.00, None, "2027-06-16", "2027-07-16", "2027-08-16", 70, 50000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://du.ac.bd"),
    ("DU-ARCH-SCI", "University of Dhaka", "BArch", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2027-06-17", "2027-07-17", "2027-08-17", 50, 90000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos","portfolio"]', "Requires drawing test.", "https://du.ac.bd"),
    ("DU-SOC-HUM", "University of Dhaka", "BA in Sociology", "HSC", "Humanities", 2.75, 2.75, None, 2.75, None, "2027-06-11", "2027-07-11", "2027-08-11", 120, 40000, "Dhaka", "Nilkhet Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://du.ac.bd"),

    # CU - University of Chittagong
    ("CU-CSE-SCI", "University of Chittagong", "BSc in Computer Science and Engineering", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2026-11-18", "2026-11-25", "2026-12-20", 80, 65000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science with physics and math.", "https://cu.ac.bd"),
    ("CU-EEE-SCI", "University of Chittagong", "BSc in Electrical and Electronic Engineering", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-20", "2027-07-20", "2027-08-20", 60, 65000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires physics, math, chemistry.", "https://cu.ac.bd"),
    ("CU-ENG-HUM", "University of Chittagong", "BA in English", "HSC", "Humanities", 2.75, 2.75, None, 2.75, None, "2027-06-15", "2027-07-15", "2027-08-15", 100, 35000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://cu.ac.bd"),
    ("CU-BBA-BUS", "University of Chittagong", "BBA", "HSC", "Business", 2.75, 2.75, None, None, 2.75, "2027-06-18", "2027-07-18", "2027-08-18", 120, 50000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Commerce background preferred.", "https://cu.ac.bd"),
    ("CU-PHARM-SCI", "University of Chittagong", "BPharm", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-22", "2027-07-22", "2027-08-22", 50, 55000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://cu.ac.bd"),
    ("CU-LAW-HUM", "University of Chittagong", "LLB (Honours)", "HSC", "Humanities", 3.00, 3.00, None, 3.00, None, "2027-06-19", "2027-07-19", "2027-08-19", 80, 40000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Admission test mandatory.", "https://cu.ac.bd"),
    ("CU-GEO-SCI", "University of Chittagong", "BSc in Geology and Mining", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-21", "2027-07-21", "2027-08-21", 40, 45000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science.", "https://cu.ac.bd"),
    ("CU-ECON-SCI", "University of Chittagong", "BSc in Economics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-16", "2027-07-16", "2027-08-16", 70, 40000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Science or business both accepted.", "https://cu.ac.bd"),
    ("CU-BIO-SCI", "University of Chittagong", "BSc in Microbiology", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-23", "2027-07-23", "2027-08-23", 45, 50000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://cu.ac.bd"),
    ("CU-STAT-SCI", "University of Chittagong", "BSc in Statistics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-24", "2027-07-24", "2027-08-24", 50, 42000, "Chittagong", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires math in HSC.", "https://cu.ac.bd"),

    # JU - Jahangirnagar University
    ("JU-CSE-SCI", "Jahangirnagar University", "BSc in Computer Science and Engineering", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-25", "2027-07-25", "2027-08-25", 70, 55000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science with physics and math.", "https://ju.ac.bd"),
    ("JU-ENG-HUM", "Jahangirnagar University", "BA in English", "HSC", "Humanities", 2.75, 2.75, None, 2.75, None, "2027-06-20", "2027-07-20", "2027-08-20", 80, 30000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://ju.ac.bd"),
    ("JU-BBA-BUS", "Jahangirnagar University", "BBA", "HSC", "Business", 2.75, 2.75, None, None, 2.75, "2027-06-22", "2027-07-22", "2027-08-22", 100, 40000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Commerce background preferred.", "https://ju.ac.bd"),
    ("JU-LAW-HUM", "Jahangirnagar University", "LLB (Honours)", "HSC", "Humanities", 3.00, 3.00, None, 3.00, None, "2027-06-26", "2027-07-26", "2027-08-26", 60, 35000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Admission test mandatory.", "https://ju.ac.bd"),
    ("JU-ENV-SCI", "Jahangirnagar University", "BSc in Environmental Science", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-27", "2027-07-27", "2027-08-27", 40, 38000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science.", "https://ju.ac.bd"),
    ("JU-PHYS-SCI", "Jahangirnagar University", "BSc in Physics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-28", "2027-07-28", "2027-08-28", 60, 32000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires physics and math in HSC.", "https://ju.ac.bd"),
    ("JU-BIO-SCI", "Jahangirnagar University", "BSc in Botany", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-29", "2027-07-29", "2027-08-29", 50, 32000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://ju.ac.bd"),
    ("JU-MATH-SCI", "Jahangirnagar University", "BSc in Mathematics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-30", "2027-07-30", "2027-08-30", 55, 32000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires math in HSC.", "https://ju.ac.bd"),
    ("JU-STAT-SCI", "Jahangirnagar University", "BSc in Statistics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-07-01", "2027-07-31", "2027-08-31", 45, 32000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires math in HSC.", "https://ju.ac.bd"),
    ("JU-ECON-SCI", "Jahangirnagar University", "BSc in Economics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-07-02", "2027-08-01", "2027-09-01", 60, 35000, "Savar, Dhaka", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Science or business both accepted.", "https://ju.ac.bd"),

    # RU - University of Rajshahi
    ("RU-CSE-SCI", "University of Rajshahi", "BSc in Computer Science and Engineering", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-20", "2027-07-20", "2027-08-20", 70, 50000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science with physics and math.", "https://ru.ac.bd"),
    ("RU-EEE-SCI", "University of Rajshahi", "BSc in Electrical and Electronic Engineering", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-20", "2027-07-20", "2027-08-20", 60, 50000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires physics, math, chemistry.", "https://ru.ac.bd"),
    ("RU-ENG-HUM", "University of Rajshahi", "BA in English", "HSC", "Humanities", 2.75, 2.75, None, 2.75, None, "2027-06-15", "2027-07-15", "2027-08-15", 90, 28000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://ru.ac.bd"),
    ("RU-BBA-BUS", "University of Rajshahi", "BBA", "HSC", "Business", 2.75, 2.75, None, None, 2.75, "2027-06-18", "2027-07-18", "2027-08-18", 100, 38000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Commerce background preferred.", "https://ru.ac.bd"),
    ("RU-LAW-HUM", "University of Rajshahi", "LLB (Honours)", "HSC", "Humanities", 3.00, 3.00, None, 3.00, None, "2027-06-22", "2027-07-22", "2027-08-22", 70, 32000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Admission test mandatory.", "https://ru.ac.bd"),
    ("RU-PHARM-SCI", "University of Rajshahi", "BPharm", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-24", "2027-07-24", "2027-08-24", 50, 45000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://ru.ac.bd"),
    ("RU-AGRI-SCI", "University of Rajshahi", "BSc in Agriculture", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-25", "2027-07-25", "2027-08-25", 80, 35000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://ru.ac.bd"),
    ("RU-ECON-SCI", "University of Rajshahi", "BSc in Economics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-26", "2027-07-26", "2027-08-26", 60, 35000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Science or business both accepted.", "https://ru.ac.bd"),
    ("RU-STAT-SCI", "University of Rajshahi", "BSc in Statistics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-27", "2027-07-27", "2027-08-27", 45, 32000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires math in HSC.", "https://ru.ac.bd"),
    ("RU-ISLM-HUM", "University of Rajshahi", "BA in Islamic Studies", "HSC", "Humanities", 2.50, 2.50, None, 2.50, None, "2027-06-28", "2027-07-28", "2027-08-28", 100, 25000, "Rajshahi", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://ru.ac.bd"),

    # SUST - Shahjalal University of Science and Technology
    ("SUST-CSE-SCI", "Shahjalal University of Science and Technology", "BSc in Computer Science and Engineering", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2026-12-01", "2026-12-08", "2027-01-05", 100, 60000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science with physics and math.", "https://sust.edu"),
    ("SUST-EEE-SCI", "Shahjalal University of Science and Technology", "BSc in Electrical and Electronic Engineering", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2027-06-10", "2027-07-10", "2027-08-10", 90, 60000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires physics, math, chemistry.", "https://sust.edu"),
    ("SUST-ENG-HUM", "Shahjalal University of Science and Technology", "BA in English", "HSC", "Humanities", 3.00, 3.00, None, 3.00, None, "2027-06-12", "2027-07-12", "2027-08-12", 80, 35000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Open to all groups.", "https://sust.edu"),
    ("SUST-BBA-BUS", "Shahjalal University of Science and Technology", "BBA", "HSC", "Business", 3.00, 3.00, None, None, 3.00, "2027-06-14", "2027-07-14", "2027-08-14", 90, 45000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Commerce background preferred.", "https://sust.edu"),
    ("SUST-LAW-HUM", "Shahjalal University of Science and Technology", "LLB (Honours)", "HSC", "Humanities", 3.25, 3.25, None, 3.25, None, "2027-06-16", "2027-07-16", "2027-08-16", 60, 40000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Admission test mandatory.", "https://sust.edu"),
    ("SUST-PHARM-SCI", "Shahjalal University of Science and Technology", "BPharm", "HSC", "Science", 3.50, 3.50, 3.50, None, None, "2027-06-18", "2027-07-18", "2027-08-18", 50, 55000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://sust.edu"),
    ("SUST-AGRI-SCI", "Shahjalal University of Science and Technology", "BSc in Agriculture", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-20", "2027-07-20", "2027-08-20", 60, 40000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires biology in HSC.", "https://sust.edu"),
    ("SUST-ECON-SCI", "Shahjalal University of Science and Technology", "BSc in Economics", "HSC", "Science", 3.25, 3.25, 3.25, None, None, "2027-06-22", "2027-07-22", "2027-08-22", 50, 38000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Science or business both accepted.", "https://sust.edu"),
    ("SUST-ENV-SCI", "Shahjalal University of Science and Technology", "BSc in Environmental Science", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-24", "2027-07-24", "2027-08-24", 40, 36000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires HSC science.", "https://sust.edu"),
    ("SUST-STAT-SCI", "Shahjalal University of Science and Technology", "BSc in Statistics", "HSC", "Science", 3.00, 3.00, 3.00, None, None, "2027-06-26", "2027-07-26", "2027-08-26", 45, 34000, "Sylhet", "Main Campus", '["HSC certificate","SSC certificate","passport photos"]', "Requires math in HSC.", "https://sust.edu"),
]


def seed():
    import sqlite3
    from .db import get_db, init_db
    init_db()
    conn = get_db()
    conn.execute("DELETE FROM programs")
    for p in PROGRAMS:
        conn.execute(
            """INSERT INTO programs (id, university, program_name, degree_level, required_group,
               min_hsc_gpa, min_ssc_gpa, min_hsc_gpa_science, min_hsc_gpa_humanities,
               min_hsc_gpa_business, application_start, application_deadline, exam_date,
               total_seats, tuition_fee_bdt, location, campus, required_documents, notes, official_website)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            p,
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(PROGRAMS)} programs")


if __name__ == "__main__":
    seed()
