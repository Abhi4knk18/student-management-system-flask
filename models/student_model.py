import sqlite3

DB_PATH = "database/student.db"

def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)

# ---------- READ ----------
def fetch_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, roll, branch, attendance FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_student(roll):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name, roll, branch, attendance FROM students WHERE roll=?",
        (roll,)
    )
    student = cur.fetchone()
    conn.close()
    return student

# ---------- CREATE ----------
def add_student(name, roll, branch):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, roll, branch, attendance) VALUES (?, ?, ?, ?)",
            (name, roll, branch, 0)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# ---------- UPDATE ----------
def update_student(name, roll, branch, attendance=None):
    conn = get_connection()
    cur = conn.cursor()

    if attendance is None:
        # old behavior (NO BREAKING CHANGE)
        cur.execute(
            "UPDATE students SET name=?, branch=? WHERE roll=?",
            (name, branch, roll)
        )
    else:
        # admin updating attendance
        cur.execute(
            "UPDATE students SET name=?, branch=?, attendance=? WHERE roll=?",
            (name, branch, attendance, roll)
        )

    conn.commit()
    conn.close()

# ---------- DELETE ----------
def delete_student(roll):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()
