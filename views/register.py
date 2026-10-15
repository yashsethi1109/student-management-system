import streamlit as st
from database import register_user


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
        <h2>📝 Register</h2>
        <p style="font-size:16px;">
            Create your account to access the AI Student Management System.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        name = st.text_input(
            "👤 Full Name"
        )

        email = st.text_input(
            "📧 Email"
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

        password = st.text_input(
            "🔒 Password",
            type="password"
        )

        st.write("")

        if st.button(
            "🚀 Register",
            use_container_width=True
        ):

            if name == "" or email == "" or password == "":
                st.error("❌ Please fill all fields.")

            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters.")

            else:

                result = register_user(
                    name,
                    email,
                    course,
                    password
                )

                if result:

                    st.success("✅ Registration Successful!")

                else:

                    st.error(
                        "❌ Email already registered. Please use another email."
                    )