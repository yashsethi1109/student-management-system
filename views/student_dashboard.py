import streamlit as st

from database import get_student_by_email


def show():

    student_name = st.session_state.get(
        "user_name",
        "Student"
    )

    student_email = st.session_state.get(
        "user_email",
        ""
    )

    student = get_student_by_email(
        student_email
    )

    st.html(
        """
<div style="
    background:linear-gradient(90deg,#0F172A,#2563EB);
    padding:22px;
    border-radius:18px;
    color:white;
    margin-bottom:20px;
    box-shadow:0 10px 25px rgba(0,0,0,0.30);
">
    <h2 style="margin:0;">
        🎓 Student Dashboard
    </h2>

    <p style="
        margin-top:8px;
        margin-bottom:0;
        font-size:16px;
    ">
        Welcome to your personal academic dashboard.
    </p>
</div>
        """
    )

    st.success(
        f"👋 Welcome, {student_name}"
    )

    if not student:

        st.warning(
            "⚠️ Your academic profile is not linked yet."
        )

        st.info(
            "Please contact the administrator and make sure "
            "your registration email matches your student "
            "profile email."
        )

        return

    st.success(
        "✅ Your academic profile is successfully linked."
    )

    st.info(
        "Student features will be added here step by step."
    )