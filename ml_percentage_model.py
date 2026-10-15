import os

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


MODEL_DIRECTORY = "models"

MODEL_PATH = os.path.join(
    MODEL_DIRECTORY,
    "student_percentage_model.pkl"
)


def create_percentage_training_dataset(
    number_of_records=2000
):

    random_generator = np.random.default_rng(42)

    current_average = random_generator.uniform(
        30,
        95,
        number_of_records
    )

    attendance_percentage = random_generator.uniform(
        40,
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
        current_average,
        total_subjects
    ):

        if average >= 75:
            failed = random_generator.integers(
                0,
                2
            )

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

    study_consistency = random_generator.uniform(
        40,
        100,
        number_of_records
    )

    improvement_component = (
        (attendance_percentage - 70) * 0.08
        + (study_consistency - 60) * 0.10
        - np.array(failed_subjects) * 1.8
    )

    random_noise = random_generator.normal(
        0,
        2.5,
        number_of_records
    )

    predicted_final_percentage = (
        current_average
        + improvement_component
        + random_noise
    )

    predicted_final_percentage = np.clip(
        predicted_final_percentage,
        0,
        100
    )

    dataset = pd.DataFrame({
        "current_average": current_average,
        "attendance_percentage": attendance_percentage,
        "total_subjects": total_subjects,
        "failed_subjects": failed_subjects,
        "study_consistency": study_consistency,
        "final_percentage": predicted_final_percentage
    })

    return dataset


def train_percentage_prediction_model():

    dataset = create_percentage_training_dataset()

    features = dataset[
        [
            "current_average",
            "attendance_percentage",
            "total_subjects",
            "failed_subjects",
            "study_consistency"
        ]
    ]

    target = dataset["final_percentage"]

    (
        x_train,
        x_test,
        y_train,
        y_test
    ) = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=250,
        max_depth=10,
        random_state=42
    )

    model.fit(
        x_train,
        y_train
    )

    predictions = model.predict(x_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    r2 = r2_score(
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

    print(
        "Percentage prediction model trained successfully."
    )

    print(
        f"Mean Absolute Error: {mae:.2f}"
    )

    print(
        f"R2 Score: {r2:.4f}"
    )

    print(
        f"Model saved at: {MODEL_PATH}"
    )


if __name__ == "__main__":

    train_percentage_prediction_model()
    