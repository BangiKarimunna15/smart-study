import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "study.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            study_date TEXT NOT NULL,
            duration INTEGER NOT NULL,
            priority TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
    create_notes_table()
    create_sessions_table()
    create_quiz_table()


def add_task(subject, topic, study_date, duration, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_tasks
        (subject, topic, study_date, duration, priority)
        VALUES (?, ?, ?, ?, ?)
    """, (subject, topic, study_date, duration, priority))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, subject, topic, study_date,
               duration, priority, completed
        FROM study_tasks
        ORDER BY study_date
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE study_tasks
        SET completed = 1
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM study_tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()
def create_notes_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_note(title, subject, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (title, subject, content)
        VALUES (?, ?, ?)
    """, (title, subject, content))

    conn.commit()
    conn.close()


def get_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, subject, content, created_at
        FROM notes
        ORDER BY created_at DESC
    """)

    notes = cursor.fetchall()

    conn.close()

    return notes


def delete_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notes
        WHERE id = ?
    """, (note_id,))

    conn.commit()
    conn.close()
def create_sessions_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration INTEGER NOT NULL,
            session_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_study_session(duration):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_sessions (duration)
        VALUES (?)
    """, (duration,))

    conn.commit()
    conn.close()


def get_total_study_minutes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(duration), 0)
        FROM study_sessions
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total
def create_quiz_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_quiz_result(subject, score, total):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_results (subject, score, total)
        VALUES (?, ?, ?)
    """, (subject, score, total))

    conn.commit()
    conn.close()


def get_quiz_results():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, score, total, completed_at
        FROM quiz_results
        ORDER BY completed_at DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results
def get_total_sessions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM study_sessions
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_completed_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM study_tasks
        WHERE completed = 1
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM study_tasks
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_daily_study_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            DATE(session_date) AS study_date,
            SUM(duration) AS total_minutes
        FROM study_sessions
        GROUP BY DATE(session_date)
        ORDER BY study_date
    """)

    data = cursor.fetchall()

    conn.close()

    return data
def get_upcoming_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, topic, study_date, duration, priority
        FROM study_tasks
        WHERE completed = 0
        ORDER BY study_date
        LIMIT 5
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks