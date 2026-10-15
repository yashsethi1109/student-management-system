import streamlit as st
from database import get_student, update_student


def show():

    student = get_student(st.session_state.selected_student)

    if student is None:
        st.error("Student not found.")
        return

    st.markdown("""
    <div style="
        background:linear-gradient(90deg,#2563EB,#7C3AED);
        padding:22px;
        border-radius:18px;
        color:white;
        box-shadow:0 10px 25px rgba(0,0,0,.35);
        margin-bottom:20px;
    ">
        <h2>✏️ Edit Student</h2>
        <p style="font-size:16px;">
            Update student details carefully.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
       "⬅️ Back to Dashboard",
       use_container_width=True,
       key="back_edit_student"
    ):
       st.session_state.dashboard_page = "dashboard"
       st.rerun()

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input(
            "👤 Full Name",
            value=student[1]
        )

        email = st.text_input(
            "📧 Email",
            value=student[2]
        )

        phone = st.text_input(
            "📱 Phone Number",
            value=student[3]
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
            ],
            index=[
                "B.Tech (CSE)",
                "B.Tech (AI)",
                "B.Tech (Civil)",
                "B.Tech (Mechanical)",
                "BCA",
                "MCA"
            ].index(student[4])
        )

    with col2:

        semester = st.selectbox(
            "📚 Semester",
            [1,2,3,4,5,6,7,8],
            index=student[5]-1
        )

        section = st.selectbox(
            "🏫 Section",
            ["A","B","C"],
            index=["A","B","C"].index(student[6])
        )

        gender = st.radio(
            "🚻 Gender",
            ["Male","Female","Other"],
            index=["Male","Female","Other"].index(student[7])
        )

        dob = st.date_input(
            "🎂 Date of Birth"
        )

    st.write("")
    st.write("")

    if st.button(
        "💾 Update Student",
        use_container_width=True
    ):

        if full_name == "" or email == "" or phone == "":
            st.error("Please fill all required fields.")

        else:

            result = update_student(
                student[0],
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

                st.success("✅ Student Updated Successfully!")

                st.session_state.dashboard_page = "view_students"

                st.rerun()

            else:

                st.error("❌ Email already exists.")