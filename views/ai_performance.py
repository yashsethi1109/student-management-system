import streamlit as st

from database import (
    get_all_students,
    get_student_performance_data,
    get_failed_subjects_count,
    get_subject_wise_performance
)

from ml_predictor import predict_student_risk
from ml_percentage_predictor import predict_final_percentage


def show():

    st.html(
        """
        <div style="
            background:linear-gradient(90deg,#0F172A,#2563EB);
            padding:22px;
            border-radius:18px;
            color:white;
            margin-bottom:20px;
            box-shadow:0 10px 25px rgba(0,0,0,0.30);
        ">
            <h2 style="margin:0;">
                🤖 AI Student Performance
            </h2>

            <p style="
                margin-top:8px;
                margin-bottom:0;
                font-size:16px;
            ">
                AI and Machine Learning analyze student performance
                using marks and attendance.
            </p>
        </div>
        """
    )

    if st.button(
        "⬅️ Back to Dashboard",
        use_container_width=True,
        key="back_ai"
    ):
        st.session_state.dashboard_page = "dashboard"
        st.rerun()

    st.write("")

    students = get_all_students()

    if not students:
        st.warning("No students available.")
        return

    student_options = {
        f"{student[1]} ({student[0]})": student[0]
        for student in students
    }

    selected_student = st.selectbox(
        "Select Student",
        options=list(student_options.keys()),
        key="ai_student_select"
    )

    student_id = student_options[selected_student]

    study_consistency = st.slider(
         "Study Consistency (%)",
         min_value=0,
         max_value=100,
         value=80,
         step=5,
         help="Estimate how consistently the student follows a regular study routine."
    )

    if st.button(
        "🤖 Analyze Performance",
        use_container_width=True,
        key="analyze_student_performance"
    ):

        student_data, attendance_data = (
            get_student_performance_data(student_id)
        )

        if student_data is None:
            st.error("Student data not found.")
            return

        average_percentage = float(
            student_data[4] or 0
        )

        total_subjects = int(
            student_data[5] or 0
        )

        total_classes = 0
        present_classes = 0

        if attendance_data is not None:

            total_classes = int(
                attendance_data[0] or 0
            )

            present_classes = int(
                attendance_data[1] or 0
            )

        attendance_percentage = 0.0

        if total_classes > 0:

            attendance_percentage = (
                present_classes / total_classes
            ) * 100

        failed_subjects = get_failed_subjects_count(
            student_id
        )
        percentage_prediction = predict_final_percentage(
            current_average=average_percentage,
            attendance_percentage=attendance_percentage,
            total_subjects=total_subjects,
            failed_subjects=failed_subjects,
            study_consistency=study_consistency
         )

        predicted_percentage = float(
            percentage_prediction["predicted_percentage"]
        )

        expected_improvement = float(
            percentage_prediction["expected_improvement"]
        )

        subject_records = get_subject_wise_performance(
            student_id
        )

        st.write("")
        st.subheader("📊 Student Performance Analysis")

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:

            st.metric(
                "Average Percentage",
                f"{average_percentage:.2f}%"
            )

        with metric_col2:

            st.metric(
                "Attendance",
                f"{attendance_percentage:.2f}%"
            )

        with metric_col3:

            st.metric(
                "Total Subjects",
                total_subjects
            )

        if (
            average_percentage >= 85
            and attendance_percentage >= 90
        ):

            performance_level = "🟢 Excellent"

            suggestions = [
                "Maintain your current academic performance.",
                "Participate in coding contests and hackathons.",
                "Start preparing for placements and technical interviews."
            ]

        elif (
            average_percentage >= 70
            and attendance_percentage >= 80
        ):

            performance_level = "🔵 Good"

            suggestions = [
                "Focus more on comparatively weak subjects.",
                "Practice programming and technical concepts daily.",
                "Aim for 85% or more in the next examination."
            ]

        elif (
            average_percentage >= 55
            and attendance_percentage >= 70
        ):

            performance_level = "🟡 Average"

            suggestions = [
                "Increase daily study and revision time.",
                "Revise difficult topics every week.",
                "Improve attendance and classroom participation."
            ]

        else:

            performance_level = "🔴 At Risk"

            suggestions = [
                "Meet the faculty mentor for academic guidance.",
                "Improve attendance immediately.",
                "Practice previous-year question papers.",
                "Create and follow a daily study schedule."
            ]

        st.write("")

        st.success(
            f"Rule-Based Performance Level: {performance_level}"
        )

        st.subheader("💡 AI Suggestions")

        for suggestion in suggestions:

            st.write(f"✅ {suggestion}")

        st.write("")
        st.divider()

        st.subheader("📚 Subject-wise Performance Analysis")

        if not subject_records:

            st.info(
                "No subject-wise marks are available for this student."
            )

        else:

            strong_subjects = []
            average_subjects = []
            weak_subjects = []

            subject_chart_data = {}

            for subject, percentage, grade in subject_records:

                percentage = float(
                    percentage or 0
                )

                subject_chart_data[subject] = round(
                    percentage,
                    2
                )

                subject_details = {
                    "subject": subject,
                    "percentage": percentage,
                    "grade": grade
                }

                if percentage >= 75:

                    strong_subjects.append(
                        subject_details
                    )

                elif percentage >= 50:

                    average_subjects.append(
                        subject_details
                    )

                else:

                    weak_subjects.append(
                        subject_details
                    )

            subject_col1, subject_col2, subject_col3 = st.columns(3)

            with subject_col1:

                st.metric(
                    "Strong Subjects",
                    len(strong_subjects)
                )

            with subject_col2:

                st.metric(
                    "Average Subjects",
                    len(average_subjects)
                )

            with subject_col3:

                st.metric(
                    "Weak Subjects",
                    len(weak_subjects)
                )

            st.write("")
            st.subheader("📊 Subject Performance Chart")

            st.bar_chart(
                subject_chart_data
            )

            st.write("")
            strong_col, average_col, weak_col = st.columns(3)

            with strong_col:

                st.subheader("🟢 Strong Subjects")

                if strong_subjects:

                    for subject in strong_subjects:

                        st.success(
                            f"{subject['subject']} — "
                            f"{subject['percentage']:.2f}% "
                            f"(Grade {subject['grade']})"
                        )

                else:

                    st.info(
                        "No strong subjects identified."
                    )

            with average_col:

                st.subheader("🟡 Average Subjects")

                if average_subjects:

                    for subject in average_subjects:

                        st.warning(
                            f"{subject['subject']} — "
                            f"{subject['percentage']:.2f}% "
                            f"(Grade {subject['grade']})"
                        )

                else:

                    st.info(
                        "No average subjects identified."
                    )

            with weak_col:

                st.subheader("🔴 Weak Subjects")

                if weak_subjects:

                    for subject in weak_subjects:

                        st.error(
                            f"{subject['subject']} — "
                            f"{subject['percentage']:.2f}% "
                            f"(Grade {subject['grade']})"
                        )

                else:

                    st.success(
                        "No weak subjects identified."
                    )

            st.write("")
            st.subheader("🎯 Personalized Subject Recommendations")

            if weak_subjects:

                for subject in weak_subjects:

                    subject_name = subject["subject"]

                    st.write(
                        f"⚠️ **{subject_name}:** "
                        "Study this subject for at least 45–60 minutes daily, "
                        "revise important concepts, solve previous-year "
                        "questions and discuss difficult topics with faculty."
                    )

            elif average_subjects:

                for subject in average_subjects:

                    subject_name = subject["subject"]

                    st.write(
                        f"📘 **{subject_name}:** "
                        "Increase weekly revision and practice more questions "
                        "to move this subject into the strong category."
                    )

            else:

                st.success(
                    "The student is performing strongly in all subjects. "
                    "Maintain regular revision and advanced practice."
                )

        st.subheader("🎯 Final Percentage Prediction")

        prediction_col1, prediction_col2, prediction_col3 = st.columns(3)

        with prediction_col1:
          st.metric(
               "Current Average",
               f"{average_percentage:.2f}%"
        )

        with prediction_col2:
           st.metric(
               "Predicted Final Percentage",
                f"{predicted_percentage:.2f}%"
        )

        with prediction_col3:
           st.metric(
                "Expected Change",
                f"{expected_improvement:+.2f}%"
        )

        if expected_improvement > 2:

           performance_trend = "📈 Improving"

           st.success(
                "The model predicts an improvement in the student's "
                "final academic percentage."
             )

        elif expected_improvement < -2:

             performance_trend = "📉 Declining"

             st.warning(
                  "The model predicts a possible decline in the student's "
                "final academic percentage."
            )
    
        else:

            performance_trend = "➡️ Stable"

            st.info(
                 "The student's predicted final percentage is close "
                 "to the current academic average."
            )

        st.write(
            f"**Performance Trend:** {performance_trend}"
        )

        st.caption(
             "This is an estimated result generated by a machine learning "
             "model trained on synthetic educational data."
        )
         
        st.write("")
        st.divider()
        st.subheader("🧠 Machine Learning Prediction")

        try:

            prediction = predict_student_risk(
                average_percentage=average_percentage,
                attendance_percentage=attendance_percentage,
                total_subjects=total_subjects,
                failed_subjects=failed_subjects
            )

            risk_level = prediction["risk_level"]

            confidence = float(
                prediction["confidence"]
            )

            probabilities = prediction[
                "probabilities"
            ]

            risk_icons = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🔴"
            }

            risk_icon = risk_icons.get(
                risk_level,
                "⚪"
            )

            ml_col1, ml_col2, ml_col3 = st.columns(3)

            with ml_col1:

                st.metric(
                    "Predicted Risk",
                    f"{risk_icon} {risk_level}"
                )

            with ml_col2:

                st.metric(
                    "Prediction Confidence",
                    f"{confidence:.2f}%"
                )

            with ml_col3:

                st.metric(
                    "Failed Subjects",
                    failed_subjects
                )

            st.write("")
            st.subheader("📊 Risk Probabilities")

            probability_chart_data = {
                level: round(
                    float(probability) * 100,
                    2
                )
                for level, probability
                in probabilities.items()
            }

            st.bar_chart(
                probability_chart_data
            )

            if risk_level == "Low":

                st.success(
                    "The ML model predicts a low academic risk. "
                    "The student should maintain consistency."
                )

            elif risk_level == "Medium":

                st.warning(
                    "The ML model predicts a medium academic risk. "
                    "Improvement in marks, attendance or weak subjects "
                    "is recommended."
                )

            else:

                st.error(
                    "The ML model predicts a high academic risk. "
                    "Immediate academic support and regular monitoring "
                    "are recommended."
                )

        except FileNotFoundError:

            st.error(
                "Machine Learning model file was not found. "
                "Run `python ml_model.py` in the terminal first."
            )

        except Exception as error:

            st.error(
                f"ML prediction could not be completed: {error}"
            )