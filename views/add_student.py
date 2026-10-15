import streamlit as st
from database import add_student


def show():

    st.markdown("""
    <div style="
        background:linear-gradient(90deg,#2563EB,#7C3AED);
        padding:22px;
        border-radius:18px;
        color:white;
        box-shadow:0 10px 25px rgba(0,0,0,.35);
        margin-bottom:20px;
    ">
        <h2>➕ Add Student</h2>
        <p style="font-size:16px;">
            Fill all student details carefully.
        </p>
    </div>
            
    """, unsafe_allow_html=True)
    
    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_add_student"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input(
            "👤 Full Name"
        )

        email = st.text_input(
            "📧 Email"
        )

        phone = st.text_input(
            "📱 Phone Number"
        )

        course = st.selectbox(
            "🎓 Course",
            [
                "B.Tech (CSE)",
                "B.Tech (AI)",
                "B.Tech (Civil)",
                "B.Tech (Mechanical)",
                "BCA",
                "MCA"
            ]
        )

    with col2:

        semester = st.selectbox(
            "📚 Semester",
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        section = st.selectbox(
            "🏫 Section",
            ["A", "B", "C"]
        )

        gender = st.radio(
            "🚻 Gender",
            ["Male", "Female", "Other"]
        )

        dob = st.date_input(
            "🎂 Date of Birth"
        )

    st.write("")
    st.write("")

    if st.button(
        "💾 Save Student",
        use_container_width=True
    ):

        if (
            full_name == ""
            or email == ""
            or phone == ""
        ):

            st.error(
                "Please fill all required fields."
            )

        else:

            result = add_student(
                full_name,
                email,
                phone,
                course,
                semester,
                section,
                gender,
                dob
            )

            if result:

                st.success(
                    "✅ Student Added Successfully!"
                )

            else:

                st.error(
                    "❌ Email already exists. Please use another email."
                )