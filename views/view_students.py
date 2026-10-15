import streamlit as st
from database import (
    get_all_students,
    delete_student,
    search_students
)


def show():

    st.markdown("""
    <style>

    .badge{
        display:inline-block;
        padding:8px 14px;
        margin:4px;
        border-radius:25px;
        font-size:15px;
        font-weight:600;
        color:white;
    }

    .course{
        background:#2563eb;
    }

    .semester{
        background:#7c3aed;
    }

    .section{
        background:#16a34a;
    }

    .gender{
        background:#334155;
    }

    div.stButton > button{
        width:100%;
        height:50px;
        border:none;
        border-radius:14px;
        font-size:16px;
        font-weight:600;
        color:white;
        background:linear-gradient(90deg,#2563eb,#7c3aed);
        transition:0.3s ease;
        box-shadow:0 8px 18px rgba(0,0,0,.25);
    }

    div.stButton > button:hover{
        transform:translateY(-3px);
        box-shadow:0 12px 25px rgba(124,58,237,.45);
    }

    </style>
    """, unsafe_allow_html=True)


    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_view_students"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    st.title("👀 View Students")

    search_text = st.text_input(
        "🔍 Search Student",
        placeholder="Search by Name, Email or Student ID..."
    )

    if search_text == "":
        students = get_all_students()
    else:
        students = search_students(search_text)

    if len(students) == 0:
        st.warning("No students found.")
        return

    st.write(f"### 👨‍🎓 Total Students : {len(students)}")

    st.divider()

    for student in students:

        with st.container():

            st.subheader(f"👤 {student[1]}")

            info_col1, info_col2 = st.columns(2)

            with info_col1:

                st.write(f"🆔 **Student ID:** {student[0]}")
                st.write(f"📧 **Email:** {student[2]}")
                st.write(f"📱 **Phone:** {student[3]}")

            with info_col2:

                st.markdown(
                    f"""
                    <span class="badge course">🎓 {student[4]}</span>
                    <span class="badge semester">📚 Semester {student[5]}</span>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <span class="badge section">🏫 Section {student[6]}</span>
                    <span class="badge gender">🚻 {student[7]}</span>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")

            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_{student[0]}",
                    use_container_width=True
                ):

                    st.session_state.selected_student = student[0]
                    st.session_state.dashboard_page = "edit_student"
                    st.rerun()

            with btn_col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{student[0]}",
                    use_container_width=True
                ):

                    delete_student(student[0])

                    st.success("✅ Student Deleted Successfully!")

                    st.rerun()

            st.divider()