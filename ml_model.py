import os

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


MODEL_DIRECTORY = "models"
MODEL_PATH = os.path.join(
    MODEL_DIRECTORY,
    "student_risk_model.pkl"
)


def create_training_dataset(number_of_records=1500):

    random_generator = np.random.default_rng(42)

    average_percentage = random_generator.uniform(
        25,
        98,
        number_of_records
    )

    attendance_percentage = random_generator.uniform(
        35,
        100,
        number_of_records
    )

    total_subjects = random_generator.integers(
        3,
        9,
        number_of_records
    )

    failed_subjects = []

    for average, subjects in zip(
        average_percentage,
        total_subjects
    ):

        if average >= 75:
            failed = random_generator.integers(0, 2)

        elif average >= 55:
            failed = random_generator.integers(
                0,
                min(3, subjects) + 1
            )

        else:
            failed = random_generator.integers(
                1,
                subjects + 1
            )

        failed_subjects.append(failed)

    risk_levels = []

    for average, attendance, failed in zip(
        average_percentage,
        attendance_percentage,
        failed_subjects
    ):

        if (
            average >= 70
            and attendance >= 75
            and failed == 0
        ):
            risk = "Low"

        elif (
            average < 45
            or attendance < 55
            or failed >= 3
        ):
            risk = "High"

        else:
            risk = "Medium"

        risk_levels.append(risk)

    dataset = pd.DataFrame({
        "average_percentage": average_percentage,
        "attendance_percentage": attendance_percentage,
        "total_subjects": total_subjects,
        "failed_subjects": failed_subjects,
        "risk_level": risk_levels
    })

    return dataset


def train_student_risk_model():

    dataset = create_training_dataset()

    features = dataset[
        [
            "average_percentage",
            "attendance_percentage",
            "total_subjects",
            "failed_subjects"
        ]
    ]

    target = dataset["risk_level"]

    (
        x_train,
        x_test,
        y_train,
        y_test
    ) = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42,
        stratify=target
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42
    )

    model.fit(
        x_train,
        y_train
    )

    predictions = model.predict(x_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    os.makedirs(
        MODEL_DIRECTORY,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("Student risk model trained successfully.")
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print(f"Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train_student_risk_model()