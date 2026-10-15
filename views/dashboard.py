import streamlit as st
from database import get_total_students
from datetime import datetime



def show():

    total_students = get_total_students()

    now = datetime.now()

    current_date = now.strftime("%d %B %Y")
    current_time = now.strftime("%I:%M %p")

    # Professional Header
    st.markdown(
        f"""
        <div style="
            background:linear-gradient(90deg,#2563EB,#7C3AED);
            padding:25px;
            border-radius:18px;
            color:white;
            box-shadow:0 10px 25px rgba(0,0,0,.35);
        ">
            <h1>🎓 AI Student Management System</h1>
            <h3>Welcome Back, {st.session_state.user_name} 👋</h3>
            <p style="font-size:16px;">
                Have a productive day 🚀
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Date & Time
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"📅 {current_date}")

    with col2:
        st.info(f"🕒 {current_time}")

    st.write("")

    # Statistics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "📚 Total Courses",
            6
        )

    st.write("---")

    st.subheader("⚡ Quick Actions")
    st.write("---")

    st.subheader("📌 Recent Activity")

    st.info("No recent activity available.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add Student", use_container_width=True):
             st.session_state.dashboard_page = "add_student"
             st.rerun()

    with col2:
         if st.button("👀 View Students", use_container_width=True):
             st.session_state.dashboard_page = "view_students"
             st.rerun()

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
       if st.button("📅 Mark Attendance", use_container_width=True):
           st.session_state.dashboard_page = "attendance"
           st.rerun()

    with col4:
       if st.button("📊 View Attendance", use_container_width=True):
            st.session_state.dashboard_page = "view_attendance"
            st.rerun()

    st.write("")

    if st.button("📘 Marks Management", use_container_width=True):
       st.session_state.dashboard_page = "marks"
       st.rerun()

    if st.button(
        "📊 View Marks",
        use_container_width=True
    ):
        st.session_state.dashboard_page = "view_marks"
        st.rerun()  

    if st.button(
       "📈 Analytics Dashboard",
       use_container_width=True,
       key="analytics_dashboard"
    ):
       st.session_state.dashboard_page = "analytics"
       st.rerun()    
    if st.button(
        "📄 Generate Report Card",
        use_container_width=True,
        key="open_report_card"
    ):
        st.session_state.dashboard_page = "report_card"
        st.rerun()   

    if st.button(
         "🤖 AI Performance",
         use_container_width=True,
         key="ai_performance"
    ):
         st.session_state.dashboard_page = "ai_performance"
         st.rerun()   

    if st.button(
        "📊 Excel Export Center",
        use_container_width=True,
        key="open_export_center"
    ):
         st.session_state.dashboard_page = "export_center"
         st.rerun()
         