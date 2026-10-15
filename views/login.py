import streamlit as st
from database import login_user
import bcrypt


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
        <h2>🔐 Login</h2>
        <p style="font-size:16px;">
            Welcome Back! Login to continue.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        email = st.text_input(
            "📧 Email"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        st.write("")

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            user = login_user(email, password)

            if user is None:

                st.error("❌ Email not found.")

            elif user is False:

                st.error("❌ Incorrect password.")

            else:

                st.session_state.logged_in = True
                st.session_state.user_name = user[1]
                st.session_state.user_role = user[5]
                st.session_state.user_email = user[2]


                st.success("✅ Login Successful!")

                st.rerun()