import streamlit as st

from database import (
    get_all_students,
    get_all_attendance,
    get_all_marks
)

from excel_export import (
    generate_students_excel,
    generate_attendance_excel,
    generate_marks_excel
)


def show():

    st.html(
        """
        <div style="
            background:linear-gradient(90deg,#0F172A,#2563EB,#7C3AED);
            padding:22px;
            border-radius:18px;
            color:white;
            margin-bottom:20px;
            box-shadow:0 10px 25px rgba(0,0,0,0.30);
        ">
            <h2 style="margin:0;">
                📊 Excel Export Center
            </h2>

            <p style="
                margin-top:8px;
                margin-bottom:0;
                font-size:16px;
            ">
                Download student, attendance and marks records in Excel format.
            </p>
        </div>
        """
    )

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_export_center"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    students = get_all_students()
    attendance_records = get_all_attendance()
    marks_records = get_all_marks()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("👨‍🎓 Students")

        st.write(
            f"Total student records: **{len(students)}**"
        )

        if students:

            students_excel = generate_students_excel(
                students
            )

            st.download_button(
                label="📥 Export Students.xlsx",
                data=students_excel.getvalue(),
                file_name="students.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True,
                key="download_students_excel"
            )

        else:

            st.info("No student records available.")

    with col2:

        st.subheader("📅 Attendance")

        st.write(
            f"Total attendance records: **{len(attendance_records)}**"
        )

        if attendance_records:

            attendance_excel = generate_attendance_excel(
                attendance_records
            )

            st.download_button(
                label="📥 Export Attendance.xlsx",
                data=attendance_excel.getvalue(),
                file_name="attendance.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True,
                key="download_attendance_excel"
            )

        else:

            st.info("No attendance records available.")

    with col3:

        st.subheader("📝 Marks")

        st.write(
            f"Total marks records: **{len(marks_records)}**"
        )

        if marks_records:

            marks_excel = generate_marks_excel(
                marks_records
            )

            st.download_button(
                label="📥 Export Marks.xlsx",
                data=marks_excel.getvalue(),
                file_name="marks.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True,
                key="download_marks_excel"
            )

        else:

            st.info("No marks records available.")