import streamlit as st
import os
from views import (
    home,
    login,
    register,
    dashboard,
    add_student,
    view_students,
    edit_student,
    attendance,
    view_attendance,
    marks,
    view_marks,
    edit_marks,
    analytics,
    report_card,
    ai_performance,
    export_center,
    student_dashboard
)

from database import create_table

st.set_page_config(
    page_title="AI Student Management System",
    page_icon="🎓",
    layout="wide"
)
# Load Custom CSS
css_file = os.path.join("assets", "style.css")

with open(css_file) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

create_table()
# Session Variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = ""    

if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "dashboard"  
    
if "selected_student" not in st.session_state:
    st.session_state.selected_student = ""      


st.sidebar.title("Navigation")

if st.session_state.logged_in:

    st.sidebar.markdown("---")

    st.sidebar.success(
        f"👤 {st.session_state.user_name}"
    )

    if st.session_state.user_role == "Admin":

        st.sidebar.info(
            "👨‍💼 Role: Admin"
        )

    else:

        st.sidebar.info(
            "🎓 Role: Student"
        )

    st.sidebar.markdown("---")

if st.session_state.logged_in:

    page = st.sidebar.radio(
        "Select Page",
        ["Dashboard"]
    )

    if page == "Dashboard":

        if st.session_state.dashboard_page == "dashboard":

            if st.session_state.user_role == "Admin":
               dashboard.show()

            else:
                 student_dashboard.show()

        elif st.session_state.dashboard_page == "add_student":
            add_student.show()

        elif st.session_state.dashboard_page == "view_students":
            view_students.show()

        elif st.session_state.dashboard_page == "edit_student":
            edit_student.show()    
        elif st.session_state.dashboard_page == "attendance":
            attendance.show()    
        elif st.session_state.dashboard_page == "view_attendance":
            view_attendance.show()    
        elif st.session_state.dashboard_page == "marks":
             marks.show()    
        elif st.session_state.dashboard_page == "view_marks":
             view_marks.show()    
        elif st.session_state.dashboard_page == "edit_marks":
             edit_marks.show()
        elif st.session_state.dashboard_page == "analytics":
             analytics.show()
        elif st.session_state.dashboard_page == "report_card":
             report_card.show()  
        elif st.session_state.dashboard_page == "ai_performance":
          ai_performance.show()     
        elif st.session_state.dashboard_page == "export_center":
          export_center.show()     
                        
                

        
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

else:

    page = st.sidebar.radio(
        "Select Page",
        ["Home", "Login", "Register"]
    )

    if page == "Home":
        home.show()

    elif page == "Login":
        login.show()

    elif page == "Register":
        register.show()