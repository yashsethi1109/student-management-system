import streamlit as st
from database import get_student_list, mark_attendance


def show():

    st.markdown(
        """
        <div style="
            background:linear-gradient(90deg,#2563EB,#7C3AED);
            padding:22px;
            border-radius:18px;
            color:white;
            box-shadow:0 10px 25px rgba(0,0,0,.35);
            margin-bottom:20px;
        ">
            <h2>📅 Attendance Management</h2>
            <p style="font-size:16px;">
                Select a student and mark daily attendance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_attendance"  
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    students = get_student_list()

    if len(students) == 0:
        st.warning("No students found. Please add students first.")
        return

    student_options = {
        f"{student_id} - {full_name}": student_id
        for student_id, full_name in students
    }

    selected_student = st.selectbox(
        "👤 Select Student",
        list(student_options.keys())
    )

    attendance_date = st.date_input(
        "📅 Attendance Date"
    )

    status = st.radio(
        "Attendance Status",
        ["Present", "Absent"],
        horizontal=True
    )

    st.write("")

    if st.button(
        "💾 Save Attendance",
        use_container_width=True
    ):

        student_id = student_options[selected_student]

        result = mark_attendance(
            student_id,
            attendance_date,
            status
        )

        if result:
            st.success("✅ Attendance Marked Successfully!")

        else:
            st.error(
                "❌ Attendance for this student is already marked on this date."
            )