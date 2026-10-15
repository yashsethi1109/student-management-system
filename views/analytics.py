import streamlit as st

from database import (
    get_total_students,
    get_total_marks_records,
    get_average_percentage,
    get_pass_marks_count,
    get_fail_marks_count,
    get_total_subjects,
    get_topper,
    get_grade_distribution,
    get_subject_wise_average,
    get_top_five_students
)


def show():

    st.html(
        """
        <div style="
            background:linear-gradient(90deg,#2563EB,#7C3AED);
            padding:22px;
            border-radius:18px;
            color:white;
            box-shadow:0 10px 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <h2 style="margin:0;">
                📊 Analytics Dashboard
            </h2>

            <p style="
                font-size:16px;
                margin-top:8px;
                margin-bottom:0;
            ">
                View student performance and academic insights.
            </p>
        </div>
        """
    )

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_analytics"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    total_students = get_total_students()
    total_records = get_total_marks_records()
    total_subjects = get_total_subjects()
    average_percentage = get_average_percentage()
    pass_count = get_pass_marks_count()
    fail_count = get_fail_marks_count()
    topper = get_topper()

    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        st.metric(
            label="👨‍🎓 Total Students",
            value=total_students
        )

    with row1_col2:
        st.metric(
            label="📄 Marks Records",
            value=total_records
        )

    with row1_col3:
        st.metric(
            label="📚 Total Subjects",
            value=total_subjects
        )

    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.metric(
            label="📈 Average Percentage",
            value=f"{average_percentage:.2f}%"
        )

    with row2_col2:
        st.metric(
            label="✅ Pass Records",
            value=pass_count
        )

    with row2_col3:
        st.metric(
            label="❌ Fail Records",
            value=fail_count
        )

    st.write("")

    if topper is None:

        st.warning(
            "No topper data available. Add marks records first."
        )

    else:

        (
            topper_name,
            topper_student_id,
            topper_subject,
            topper_percentage,
            topper_grade
        ) = topper



    st.write("")
    st.subheader("📊 Grade Distribution")

    grade_data = get_grade_distribution()

    if not grade_data:
        st.info("No grade data available.")
    else:
        grade_chart_data = {
            grade: count
            for grade, count in grade_data
        }

        st.bar_chart(grade_chart_data)

    st.write("")
    st.subheader("✅ Pass vs ❌ Fail")

    pass_count = get_pass_marks_count()
    fail_count = get_fail_marks_count()

    chart_data = {
        "Pass": pass_count,
        "Fail": fail_count
    }

    st.bar_chart(chart_data)    


    st.write("")
    st.subheader("📚 Subject-wise Average Percentage")

    subject_average_data = get_subject_wise_average()

    if not subject_average_data:
        st.info("No subject performance data available.")
    else:
        subject_chart_data = {
            subject: round(float(average), 2)
            for subject, average in subject_average_data
        }

        st.bar_chart(subject_chart_data)

    st.write("")
    st.subheader("🏆 Top 5 Students Leaderboard")

    top_students = get_top_five_students()

    if not top_students:
         st.info("No student performance data available.")
    else:

         leaderboard = []

         rank = 1

         for name, student_id, percentage in top_students:

              leaderboard.append({
                   "Rank": rank,
                   "Student ID": student_id,
                   "Student Name": name,
                   "Average %": f"{percentage:.2f}%"
               })

              rank += 1

         st.dataframe(
             leaderboard,
             use_container_width=True,
             hide_index=True
         )

    st.html(
            f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:16px;
                border:1px solid #374151;
                box-shadow:0 8px 20px rgba(0,0,0,0.25);
                margin-top:10px;
            ">

                <h3 style="
                    color:#F9FAFB;
                    margin-top:0;
                ">
                    🥇 Current Top Performer
                </h3>

                <div style="
                    display:grid;
                    grid-template-columns:repeat(2,1fr);
                    gap:14px;
                    margin-top:16px;
                ">

                    <div style="
                        background:#1F2937;
                        padding:14px;
                        border-radius:10px;
                    ">
                        <p style="color:#9CA3AF; margin:0;">
                            Student Name
                        </p>

                        <p style="
                            color:#F9FAFB;
                            font-weight:bold;
                            margin-top:5px;
                            margin-bottom:0;
                        ">
                            {topper_name}
                        </p>
                    </div>

                    <div style="
                        background:#1F2937;
                        padding:14px;
                        border-radius:10px;
                    ">
                        <p style="color:#9CA3AF; margin:0;">
                            Student ID
                        </p>

                        <p style="
                            color:#F9FAFB;
                            font-weight:bold;
                            margin-top:5px;
                            margin-bottom:0;
                        ">
                            {topper_student_id}
                        </p>
                    </div>

                    <div style="
                        background:#1F2937;
                        padding:14px;
                        border-radius:10px;
                    ">
                        <p style="color:#9CA3AF; margin:0;">
                            Subject
                        </p>

                        <p style="
                            color:#F9FAFB;
                            font-weight:bold;
                            margin-top:5px;
                            margin-bottom:0;
                        ">
                            {topper_subject}
                        </p>
                    </div>

                    <div style="
                        background:#1F2937;
                        padding:14px;
                        border-radius:10px;
                    ">
                        <p style="color:#9CA3AF; margin:0;">
                            Performance
                        </p>

                        <p style="
                            color:#F9FAFB;
                            font-weight:bold;
                            margin-top:5px;
                            margin-bottom:0;
                        ">
                            {topper_percentage:.2f}% — Grade {topper_grade}
                        </p>
                    </div>

                </div>

            </div>
            """
        )