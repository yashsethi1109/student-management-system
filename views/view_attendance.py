import streamlit as st
from database import get_all_attendance


def show():

    st.markdown(
        """
        <div style="
            background:linear-gradient(90deg,#2563EB,#7C3AED);
            padding:22px;
            border-radius:18px;
            color:white;
            box-shadow:0 10px 25px rgba(0,0,0,.35);
            margin-bottom:20px;
        ">
            <h2>📊 View Attendance</h2>
            <p style="font-size:16px;">
                View student attendance records.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_view_attendance"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")
    
    records = get_all_attendance()

    if len(records) == 0:
        st.warning("No attendance records found.")
        return

    st.write(f"### Total Records: {len(records)}")
    st.divider()

    for record in records:

        attendance_id = record[0]
        student_id = record[1]
        full_name = record[2]
        attendance_date = record[3]
        status = record[4]

        with st.container():

            st.subheader(f"👤 {full_name}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"🆔 **Student ID:** {student_id}")
                st.write(f"📅 **Date:** {attendance_date}")

            with col2:

                if status == "Present":
                    st.success("✅ Present")
                else:
                    st.error("❌ Absent")

            st.divider()