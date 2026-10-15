import os
import sqlite3
import bcrypt

from datetime import datetime

DB_FOLDER = "database"
DB_PATH = os.path.join(DB_FOLDER, "student.db")


def create_connection():
    # The database folder is not stored in Git, so create it if it is missing
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        course TEXT,
        password TEXT
    )
    """)

    # student management table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        course TEXT,
        semester INTEGER,
        section TEXT,
        gender TEXT,
        dob TEXT,
        created_at TEXT
    )
    """)

    # Attendance Management Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        attendance_date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
        created_at TEXT,
        UNIQUE(student_id, attendance_date),
        FOREIGN KEY(student_id) REFERENCES student_details(student_id)
    )
    """)

    # Marks Management Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        subject TEXT NOT NULL,
        internal_marks INTEGER NOT NULL,
        external_marks INTEGER NOT NULL,
        total_marks INTEGER NOT NULL,
        percentage REAL NOT NULL,
        grade TEXT NOT NULL,
        created_at TEXT,
        UNIQUE(student_id, subject),
        FOREIGN KEY(student_id) REFERENCES student_details(student_id)
    )
    """)

    # Add role column if it does not already exist
    try:
        cursor.execute("""
            ALTER TABLE students
            ADD COLUMN role TEXT DEFAULT 'Admin'
        """)
    except sqlite3.OperationalError:
        # Column already exists
        pass

    conn.commit()
    conn.close()


def register_user(
    name,
    email,
    course,
    password,
    role="Student"
):
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cursor.execute(
            """
            INSERT INTO students (
                name,
                email,
                course,
                password,
                role
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                course,
                hashed_password,
                role
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            course,
            password,
            role
        FROM students
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    stored_password = user[4].encode("utf-8")

    if bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password
    ):
        return user

    return False


def get_total_students():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def add_student(full_name, email, phone, course, semester, section, gender, dob):

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Auto Student ID
        cursor.execute("SELECT MAX(id) FROM student_details")

        last_id = cursor.fetchone()[0]

        if last_id is None:
            last_id = 0

        student_id = f"STU{last_id + 1:04d}"

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO student_details
        (
            student_id,
            full_name,
            email,
            phone,
            course,
            semester,
            section,
            gender,
            dob,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            full_name,
            email,
            phone,
            course,
            semester,
            section,
            gender,
            str(dob),
            created_at
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError as e:
        print("Database Error :", e)
        return False

    finally:
        conn.close()


def get_all_students():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        student_id,
        full_name,
        email,
        phone,
        course,
        semester,
        section,
        gender
    FROM student_details
    ORDER BY id DESC
    """)

    students = cursor.fetchall()

    conn.close()

    return students


def get_student(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        student_id,
        full_name,
        email,
        phone,
        course,
        semester,
        section,
        gender,
        dob
    FROM student_details
    WHERE student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return student


def update_student(
    student_id,
    full_name,
    email,
    phone,
    course,
    semester,
    section,
    gender,
    dob
):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        UPDATE student_details
        SET
            full_name = ?,
            email = ?,
            phone = ?,
            course = ?,
            semester = ?,
            section = ?,
            gender = ?,
            dob = ?
        WHERE student_id = ?
        """,
        (
            full_name,
            email,
            phone,
            course,
            semester,
            section,
            gender,
            str(dob),
            student_id
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def delete_student(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM student_details
    WHERE student_id = ?
    """, (student_id,))

    conn.commit()
    conn.close()

    return True


def search_students(search_text):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        student_id,
        full_name,
        email,
        phone,
        course,
        semester,
        section,
        gender
    FROM student_details
    WHERE
        full_name LIKE ?
        OR email LIKE ?
        OR student_id LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    students = cursor.fetchall()

    conn.close()

    return students


def get_student_list():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        student_id,
        full_name
    FROM student_details
    ORDER BY full_name
    """)

    students = cursor.fetchall()

    conn.close()

    return students


def mark_attendance(student_id, attendance_date, status):

    conn = create_connection()
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        cursor.execute("""
        INSERT INTO attendance
        (
            student_id,
            attendance_date,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            student_id,
            str(attendance_date),
            status,
            created_at
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def get_attendance():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        attendance.student_id,
        student_details.full_name,
        attendance.attendance_date,
        attendance.status
    FROM attendance
    INNER JOIN student_details
    ON attendance.student_id = student_details.student_id
    ORDER BY attendance.attendance_date DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_all_attendance():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        attendance.id,
        attendance.student_id,
        student_details.full_name,
        attendance.attendance_date,
        attendance.status
    FROM attendance
    INNER JOIN student_details
        ON attendance.student_id = student_details.student_id
    ORDER BY attendance.attendance_date DESC, attendance.id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def add_marks(
    student_id,
    subject,
    internal_marks,
    external_marks
):

    conn = create_connection()
    cursor = conn.cursor()

    total_marks = internal_marks + external_marks

    percentage = (total_marks / 100) * 100

    if percentage >= 90:
        grade = "A+"

    elif percentage >= 80:
        grade = "A"

    elif percentage >= 70:
        grade = "B"

    elif percentage >= 60:
        grade = "C"

    elif percentage >= 50:
        grade = "D"

    else:
        grade = "F"

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        cursor.execute("""
        INSERT INTO marks
        (
            student_id,
            subject,
            internal_marks,
            external_marks,
            total_marks,
            percentage,
            grade,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            subject,
            internal_marks,
            external_marks,
            total_marks,
            percentage,
            grade,
            created_at
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def get_all_marks():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            marks.id,
            marks.student_id,
            student_details.full_name,
            marks.subject,
            marks.internal_marks,
            marks.external_marks,
            marks.total_marks,
            marks.percentage,
            marks.grade,
            marks.created_at
        FROM marks

        INNER JOIN student_details
        ON marks.student_id = student_details.student_id

        ORDER BY marks.id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def delete_marks(marks_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM marks
        WHERE id = ?
        """,
        (marks_id,)
    )

    conn.commit()
    conn.close()

    return True


def get_marks_by_id(marks_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            student_id,
            subject,
            internal_marks,
            external_marks,
            total_marks,
            percentage,
            grade,
            created_at
        FROM marks
        WHERE id = ?
        """,
        (marks_id,)
    )

    record = cursor.fetchone()

    conn.close()

    return record


def update_marks(
    marks_id,
    subject,
    internal_marks,
    external_marks
):

    conn = create_connection()
    cursor = conn.cursor()

    total_marks = internal_marks + external_marks
    percentage = float(total_marks)

    if percentage >= 90:
        grade = "A+"

    elif percentage >= 80:
        grade = "A"

    elif percentage >= 70:
        grade = "B"

    elif percentage >= 60:
        grade = "C"

    elif percentage >= 50:
        grade = "D"

    else:
        grade = "F"

    try:

        cursor.execute(
            """
            UPDATE marks
            SET
                subject = ?,
                internal_marks = ?,
                external_marks = ?,
                total_marks = ?,
                percentage = ?,
                grade = ?
            WHERE id = ?
            """,
            (
                subject,
                internal_marks,
                external_marks,
                total_marks,
                percentage,
                grade,
                marks_id
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def search_marks(search_text):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            marks.id,
            marks.student_id,
            student_details.full_name,
            marks.subject,
            marks.internal_marks,
            marks.external_marks,
            marks.total_marks,
            marks.percentage,
            marks.grade,
            marks.created_at

        FROM marks

        INNER JOIN student_details
        ON marks.student_id = student_details.student_id

        WHERE
            student_details.full_name LIKE ?
            OR marks.student_id LIKE ?
            OR marks.subject LIKE ?

        ORDER BY marks.id DESC
    """,
    (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    records = cursor.fetchall()

    conn.close()

    return records


def get_total_marks_records():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM marks
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_average_percentage():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(percentage)
        FROM marks
    """)

    average = cursor.fetchone()[0]

    conn.close()

    if average is None:
        return 0

    return round(average, 2)


def get_pass_marks_count():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM marks
        WHERE percentage >= 50
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_fail_marks_count():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM marks
        WHERE percentage < 50
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_subjects():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT subject)
        FROM marks
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_topper():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_details.full_name,
            marks.student_id,
            marks.subject,
            marks.percentage,
            marks.grade

        FROM marks

        INNER JOIN student_details
        ON marks.student_id = student_details.student_id

        ORDER BY marks.percentage DESC

        LIMIT 1
    """)

    topper = cursor.fetchone()

    conn.close()

    return topper


def get_grade_distribution():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT grade, COUNT(*)
        FROM marks
        GROUP BY grade
        ORDER BY grade
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_subject_wise_average():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, AVG(percentage)
        FROM marks
        GROUP BY subject
        ORDER BY AVG(percentage) DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_top_five_students():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_details.full_name,
            marks.student_id,
            AVG(marks.percentage) AS average_percentage
        FROM marks
        JOIN student_details
        ON marks.student_id = student_details.student_id
        GROUP BY marks.student_id, student_details.full_name
        ORDER BY average_percentage DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_student_report_data(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student_id,
            full_name,
            email,
            phone,
            course,
            semester,
            section,
            gender,
            dob
        FROM student_details
        WHERE student_id = ?
        """,
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.execute(
        """
        SELECT
            subject,
            internal_marks,
            external_marks,
            total_marks,
            percentage,
            grade
        FROM marks
        WHERE student_id = ?
        ORDER BY subject
        """,
        (student_id,)
    )

    marks = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_classes,
            SUM(
                CASE
                    WHEN status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS present_classes
        FROM attendance
        WHERE student_id = ?
        """,
        (student_id,)
    )

    attendance = cursor.fetchone()

    conn.close()

    return student, marks, attendance


def get_student_performance_data(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student_details.student_id,
            student_details.full_name,
            student_details.course,
            student_details.semester,
            AVG(marks.percentage) AS average_percentage,
            COUNT(marks.id) AS total_subjects
        FROM student_details
        LEFT JOIN marks
        ON student_details.student_id = marks.student_id
        WHERE student_details.student_id = ?
        GROUP BY
            student_details.student_id,
            student_details.full_name,
            student_details.course,
            student_details.semester
        """,
        (student_id,)
    )

    student_data = cursor.fetchone()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_classes,
            SUM(
                CASE
                    WHEN status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS present_classes
        FROM attendance
        WHERE student_id = ?
        """,
        (student_id,)
    )

    attendance_data = cursor.fetchone()

    conn.close()

    return student_data, attendance_data


def get_failed_subjects_count(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM marks
        WHERE student_id = ?
        AND percentage < 40
        """,
        (student_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return 0

    return result[0] or 0


def get_subject_wise_performance(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            subject,
            percentage,
            grade
        FROM marks
        WHERE student_id = ?
        ORDER BY percentage DESC
        """,
        (student_id,)
    )

    records = cursor.fetchall()

    conn.close()

    return records


def get_student_by_email(email):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student_id,
            full_name,
            email,
            phone,
            course,
            semester,
            section,
            gender,
            dob,
            created_at
        FROM student_details
        WHERE email = ?
        """,
        (email,)
    )

    student = cursor.fetchone()

    conn.close()

    return student
