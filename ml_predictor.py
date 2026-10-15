import os

import joblib
import pandas as pd


MODEL_PATH = os.path.join(
    "models",
    "student_risk_model.pkl"
)


def load_student_risk_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "ML model file not found. Run ml_model.py first."
        )

    model = joblib.load(MODEL_PATH)

    return model


def predict_student_risk(
    average_percentage,
    attendance_percentage,
    total_subjects,
    failed_subjects
):

    model = load_student_risk_model()

    input_data = pd.DataFrame(
        [
            {
                "average_percentage": average_percentage,
                "attendance_percentage": attendance_percentage,
                "total_subjects": total_subjects,
                "failed_subjects": failed_subjects
            }
        ]
    )

    predicted_risk = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    class_names = model.classes_

    probability_data = {
        class_name: float(probability)
        for class_name, probability in zip(
            class_names,
            probabilities
        )
    }

    confidence = probability_data[predicted_risk] * 100

    return {
        "risk_level": predicted_risk,
        "confidence": confidence,
        "probabilities": probability_data
    }