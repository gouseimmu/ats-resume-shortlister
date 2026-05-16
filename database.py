import sqlite3

import pandas as pd


DB_PATH = "ats_enterprise.db"


INTERVIEW_COLUMNS = {
    "name": "TEXT",
    "email": "TEXT",
    "date": "TEXT",
    "time": "TEXT",
    "mode": "TEXT",
    "link": "TEXT",
    "interviewer": "TEXT",
    "status": "TEXT",
    "role": "TEXT",
    "notes": "TEXT",
    "subject": "TEXT",
    "body": "TEXT",
    "from_email": "TEXT",
    "cc_email": "TEXT",
    "google_calendar_url": "TEXT",
}


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS interviews
           (id INTEGER PRIMARY KEY AUTOINCREMENT)"""
    )
    existing = {row[1] for row in c.execute("PRAGMA table_info(interviews)").fetchall()}
    for column, col_type in INTERVIEW_COLUMNS.items():
        if column not in existing:
            c.execute(f"ALTER TABLE interviews ADD COLUMN {column} {col_type}")
    conn.commit()
    conn.close()


def save_interview(data):
    init_db()
    columns = list(INTERVIEW_COLUMNS.keys())
    values = [data.get(column, "") for column in columns]
    placeholders = ", ".join(["?"] * len(columns))
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        f"INSERT INTO interviews ({', '.join(columns)}) VALUES ({placeholders})",
        values,
    )
    conn.commit()
    conn.close()


def get_interviews():
    init_db()
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM interviews ORDER BY date ASC, time ASC", conn)
    conn.close()
    return df


def delete_interview(interview_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM interviews WHERE id = ?", (interview_id,))
    conn.commit()
    conn.close()
