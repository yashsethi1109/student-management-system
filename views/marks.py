import streamlit as st
from database import get_student_list, add_marks


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
            <h2>📘 Marks Management</h2>
            <p style="font-size:16px;">
                Select a student and enter subject marks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_marks"
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

    subject = st.selectbox(
        "📚 Subject",
        [
            "Python",
            "Artificial Intelligence",
            "Database Management System",
            "Computer Networks",
            "Software Engineering",
            "Cloud Computing"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        internal_marks = st.number_input(
            "📝 Internal Marks",
            min_value=0,
            max_value=30,
            value=0,
            step=1
        )

    with col2:
        external_marks = st.number_input(
            "📄 External Marks",
            min_value=0,
            max_value=70,
            value=0,
            step=1
        )

    total_marks = internal_marks + external_marks

    st.info(f"📊 Total Marks: {total_marks}/100")

    if st.button(
        "💾 Save Marks",
        use_container_width=True
    ):

        student_id = student_options[selected_student]

        result = add_marks(
            student_id,
            subject,
            internal_marks,
            external_marks
        )

        if result:
            st.success("✅ Marks Added Successfully!")

        else:
            st.error(
                "❌ Marks for this student and subject already exist."
            )