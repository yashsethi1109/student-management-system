import streamlit as st

from database import (
    get_all_marks,
    delete_marks,
    search_marks
)


def show():

    # -----------------------------
    # Page Header
    # -----------------------------
    st.html(
        """
        <div style="
            background:linear-gradient(90deg,#2563EB,#7C3AED);
            padding:22px;
            border-radius:18px;
            color:white;
            box-shadow:0 10px 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <h2 style="margin:0;">
                📊 View Marks
            </h2>

            <p style="
                font-size:16px;
                margin-top:8px;
                margin-bottom:0;
            ">
                View, edit and delete students' marks records.
            </p>
        </div>
        """
    )

    # -----------------------------
    # Back Button
    # -----------------------------
    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_view_marks"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    # -----------------------------
    # Get Marks Records
    # -----------------------------
    records = get_all_marks()

    st.metric(
        label="📚 Total Marks Records",
        value=len(records)
    )
    # -----------------------------
    # Search Box
    # -----------------------------
    search = st.text_input(
        "🔍 Search by Student Name, Student ID or Subject",
         placeholder="Type student name, ID or subject..."
    )

    if search.strip():
         records = search_marks(search)

    st.write("")

    # -----------------------------
    # Empty Records Validation
    # -----------------------------
    if len(records) == 0:
        st.warning("No marks records found.")
        return

    # -----------------------------
    # Initialize Delete State
    # -----------------------------
    if "delete_marks_id" not in st.session_state:
        st.session_state.delete_marks_id = None

    # -----------------------------
    # Display Records
    # -----------------------------
    for record in records:

        (
            marks_id,
            student_id,
            full_name,
            subject,
            internal_marks,
            external_marks,
            total_marks,
            percentage,
            grade,
            created_at
        ) = record

        # -----------------------------
        # Marks Card
        # -----------------------------
        html_card = f"""
        <div style="
            background:#111827;
            padding:20px;
            border-radius:16px;
            margin-bottom:12px;
            border:1px solid #374151;
            box-shadow:0 8px 20px rgba(0,0,0,0.25);
        ">

            <h3 style="
                color:#F9FAFB;
                margin-top:0;
                margin-bottom:8px;
            ">
                👨‍🎓 {full_name}
            </h3>

            <p style="
                color:#9CA3AF;
                margin-top:0;
            ">
                🆔 Student ID: {student_id}
            </p>

            <hr style="
                border:none;
                border-top:1px solid #374151;
                margin-top:14px;
                margin-bottom:14px;
            ">

            <div style="
                display:grid;
                grid-template-columns:repeat(3, 1fr);
                gap:12px;
            ">

                <div style="
                    background:#1F2937;
                    padding:12px;
                    border-radius:10px;
                ">
                    <p style="
                        color:#9CA3AF;
                        margin:0;
                        font-size:13px;
                    ">
                        📚 Subject
                    </p>

                    <p style="
                        color:#F9FAFB;
                        margin-top:5px;
                        margin-bottom:0;
                        font-weight:bold;
                    ">
                        {subject}
                    </p>
                </div>

                <div style="
                    background:#1F2937;
                    padding:12px;
                    border-radius:10px;
                ">
                    <p style="
                        color:#9CA3AF;
                        margin:0;
                        font-size:13px;
                    ">
                        📝 Internal Marks
                    </p>

                    <p style="
                        color:#F9FAFB;
                        margin-top:5px;
                        margin-bottom:0;
                        font-weight:bold;
                    ">
                        {internal_marks}/30
                    </p>
                </div>

                <div style="
                    background:#1F2937;
                    padding:12px;
                    border-radius:10px;
                ">
                    <p style="
                        color:#9CA3AF;
                        margin:0;
                        font-size:13px;
                    ">
                        📄 External Marks
                    </p>

                    <p style="
                        color:#F9FAFB;
                        margin-top:5px;
                        margin-bottom:0;
                        font-weight:bold;
                    ">
                        {external_marks}/70
                    </p>
                </div>

                <div style="
                    background:#1F2937;
                    padding:12px;
                    border-radius:10px;
                ">
                    <p style="
                        color:#9CA3AF;
                        margin:0;
                        font-size:13px;
                    ">
                        📊 Total Marks
                    </p>

                    <p style="
                        color:#F9FAFB;
                        margin-top:5px;
                        margin-bottom:0;
                        font-weight:bold;
                    ">
                        {total_marks}/100
                    </p>
                </div>

                <div style="
                    background:#1F2937;
                    padding:12px;
                    border-radius:10px;
                ">
                    <p style="
                        color:#9CA3AF;
                        margin:0;
                        font-size:13px;
                    ">
                        📈 Percentage
                    </p>

                    <p style="
                        color:#F9FAFB;
                        margin-top:5px;
                        margin-bottom:0;
                        font-weight:bold;
                    ">
                        {percentage:.2f}%
                    </p>
                </div>

                <div style="
                    background:#1F2937;
                    padding:12px;
                    border-radius:10px;
                ">
                    <p style="
                        color:#9CA3AF;
                        margin:0;
                        font-size:13px;
                    ">
                        🏆 Grade
                    </p>

                    <p style="
                        color:#F9FAFB;
                        margin-top:5px;
                        margin-bottom:0;
                        font-weight:bold;
                    ">
                        {grade}
                    </p>
                </div>

            </div>

            <p style="
                color:#6B7280;
                margin-top:14px;
                margin-bottom:0;
                font-size:13px;
            ">
                Added on: {created_at}
            </p>

        </div>
        """

        st.html(html_card)

        # -----------------------------
        # Edit and Delete Buttons
        # -----------------------------
        edit_column, delete_column = st.columns(2)

        with edit_column:

            if st.button(
                "✏️ Edit Marks",
                use_container_width=True,
                key=f"edit_marks_{marks_id}"
            ):
                st.session_state.selected_marks_id = marks_id
                st.session_state.dashboard_page = "edit_marks"
                st.rerun()

        with delete_column:

            if st.button(
                "🗑️ Delete Marks",
                use_container_width=True,
                key=f"delete_marks_{marks_id}"
            ):
                st.session_state.delete_marks_id = marks_id
                st.rerun()

        # -----------------------------
        # Delete Confirmation
        # -----------------------------
        if st.session_state.delete_marks_id == marks_id:

            st.warning(
                f"Are you sure you want to delete "
                f"{full_name}'s marks for {subject}?"
            )

            confirm_column, cancel_column = st.columns(2)

            with confirm_column:

                if st.button(
                    "✅ Yes, Delete",
                    use_container_width=True,
                    key=f"confirm_delete_marks_{marks_id}"
                ):

                    result = delete_marks(marks_id)

                    if result:
                        st.session_state.delete_marks_id = None
                        st.success(
                            "Marks record deleted successfully."
                        )
                        st.rerun()

                    else:
                        st.error(
                            "Unable to delete marks record."
                        )

            with cancel_column:

                if st.button(
                    "❌ Cancel",
                    use_container_width=True,
                    key=f"cancel_delete_marks_{marks_id}"
                ):
                    st.session_state.delete_marks_id = None
                    st.rerun()

        st.write("")