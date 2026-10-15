import streamlit as st


def show():

    st.markdown("""
    <div style="
        background:linear-gradient(90deg,#2563EB,#7C3AED);
        padding:30px;
        border-radius:20px;
        color:white;
        text-align:center;
        box-shadow:0 12px 30px rgba(0,0,0,.35);
        margin-bottom:25px;
    ">
        <h1>🎓 AI Student Management System</h1>
        <p style="font-size:18px;">
            Smart • Secure • Modern Student Management Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 👋 Welcome

    Welcome to the **AI Student Management System**.

    This application is built using **Python**, **Streamlit**, **SQLite**, and **Artificial Intelligence** technologies to manage student information efficiently through a modern dashboard.
    """)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### 📌 Core Modules

👨‍🎓 Student Management

📋 Attendance Management

📝 Marks Management

📊 Reports & Analytics
""")

    with col2:

        st.success("""
### 🤖 AI Features

🧠 AI Prediction

📈 Smart Analytics

🔍 Live Search

⚡ Fast Dashboard
""")

    st.write("")

    st.markdown("---")

    st.subheader("🚀 Why Choose This System?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎓 Student Records", "Secure")

    with col2:
        st.metric("⚡ Performance", "Fast")

    with col3:
        st.metric("🤖 AI Ready", "Enabled")

    st.markdown("---")

    st.success(
        "💙 Manage student records easily with a modern, secure and AI-powered management system."
    )