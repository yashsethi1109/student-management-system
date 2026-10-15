import os
import streamlit as st

from database import (
    get_all_students,
    get_student_report_data
)

from report_generator import generate_report


def show():

    st.html(
        """
        <div style="
            background:linear-gradient(90deg,#0F766E,#2563EB);
            padding:22px;
            border-radius:18px;
            color:white;
            margin-bottom:20px;
        ">
            <h2 style="margin:0;">
                📄 Student Report Card
            </h2>

            <p style="margin-top:8px; margin-bottom:0;">
                Generate and download a student's academic report.
            </p>
        </div>
        """
    )

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_report_card"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    students = get_all_students()

    if not students:

        st.warning(
            "No students available. Add a student first."
        )

        return

    student_options = {
        f"{student[1]} ({student[0]})": student[0]
        for student in students
    }

    selected_student = st.selectbox(
        "Select Student",
        options=list(student_options.keys())
    )

    selected_student_id = student_options[selected_student]

    if st.button(
        "📄 Generate Report Card",
        use_container_width=True,
        key="generate_report_card"
    ):

        student, marks, attendance = get_student_report_data(
            selected_student_id
        )

        if student is None:

            st.error("Student record not found.")

            return

        if not marks:

            st.warning(
                "No marks records are available for this student."
            )

            return

        os.makedirs(
            "generated_reports",
            exist_ok=True
        )

        pdf_path = os.path.join(
            "generated_reports",
            f"{selected_student_id}_report_card.pdf"
        )

        generate_report(
            student,
            marks,
            attendance,
            pdf_path
        )

        st.session_state.generated_pdf_path = pdf_path
        st.session_state.generated_student_id = selected_student_id

        st.success(
            "Report card generated successfully."
        )

    pdf_path = st.session_state.get(
        "generated_pdf_path"
    )

    generated_student_id = st.session_state.get(
        "generated_student_id"
    )

    if (
        pdf_path
        and generated_student_id == selected_student_id
        and os.path.exists(pdf_path)
    ):

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="⬇️ Download Report Card",
                data=pdf_file.read(),
                file_name=f"{selected_student_id}_report_card.pdf",
                mime="application/pdf",
                use_container_width=True,
                key=f"download_{selected_student_id}"
            )