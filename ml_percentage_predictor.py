import os

import joblib
import pandas as pd


MODEL_PATH = os.path.join(
    "models",
    "student_percentage_model.pkl"
)


def load_percentage_model():

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Percentage prediction model not found."
        )

    return joblib.load(MODEL_PATH)


def predict_final_percentage(

    current_average,
    attendance_percentage,
    total_subjects,
    failed_subjects,
    study_consistency=80

):

    model = load_percentage_model()

    dataframe = pd.DataFrame([

        {

            "current_average": current_average,

            "attendance_percentage": attendance_percentage,

            "total_subjects": total_subjects,

            "failed_subjects": failed_subjects,

            "study_consistency": study_consistency

        }

    ])

    prediction = model.predict(dataframe)[0]

    prediction = max(
        0,
        min(
            100,
            float(prediction)
        )
    )

    improvement = prediction - current_average

    return {

        "predicted_percentage": prediction,

        "expected_improvement": improvement

    }