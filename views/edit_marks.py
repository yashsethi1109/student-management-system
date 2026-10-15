import streamlit as st

from database import (
    get_marks_by_id,
    update_marks
)


def show():

    st.markdown(
        """
        <div style="
            background:linear-gradient(90deg,#2563EB,#7C3AED);
            padding:22px;
            border-radius:18px;
            color:white;
            margin-bottom:20px;
        ">
            <h2>✏️ Edit Marks</h2>
            <p>Update student marks.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Back Button
    if st.button(
        "⬅️ Back to View Marks",
        use_container_width=True,
        key="back_edit_marks"
    ):
        st.session_state.dashboard_page = "view_marks"
        st.rerun()

    st.write("")

    if "selected_marks_id" not in st.session_state:
        st.error("No marks record selected.")
        return

    record = get_marks_by_id(
        st.session_state.selected_marks_id
    )

    if record is None:
        st.error("Marks record not found.")
        return

    (
        marks_id,
        student_id,
        subject,
        internal_marks,
        external_marks,
        total_marks,
        percentage,
        grade,
        created_at
    ) = record

    subjects = [
        "Python",
        "Artificial Intelligence",
        "Database Management System",
        "Computer Networks",
        "Software Engineering",
        "Cloud Computing"
    ]

    subject = st.selectbox(
        "📚 Subject",
        subjects,
        index=subjects.index(subject)
    )

    col1, col2 = st.columns(2)

    with col1:
        internal_marks = st.number_input(
            "📝 Internal Marks",
            0,
            30,
            value=internal_marks
        )

    with col2:
        external_marks = st.number_input(
            "📄 External Marks",
            0,
            70,
            value=external_marks
        )

    st.info(
        f"📊 Total Marks : {internal_marks + external_marks}/100"
    )

    if st.button(
        "💾 Update Marks",
        use_container_width=True
    ):

        result = update_marks(
            marks_id,
            subject,
            internal_marks,
            external_marks
        )

        if result:

            st.success(
                "✅ Marks Updated Successfully!"
            )

            st.session_state.dashboard_page = "view_marks"

            st.rerun()

        else:

            st.error(
                "Unable to update marks."
            )
            