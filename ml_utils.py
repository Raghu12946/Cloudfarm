import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Path to your dataset
DATASET_PATH = "C:\\Users\\nanda\\OneDrive\\Desktop\\CloudFarm-main\\CloudFarm-main\\cloudfarm_app\\filled_crop_fertilizer_dataset - filled_crop_fertilizer_dataset.csv.csv"


def load_and_train_models():
    """Load data, train ensemble models, and return them along with encoders."""
    # Load dataset
    data = pd.read_csv(DATASET_PATH)

    # Drop humidity only if present
    if "humidity" in data.columns:
        data = data.drop(columns=["humidity"])

    # Encode target columns
    label_encoder_crop = LabelEncoder()
    label_encoder_fertilizer = LabelEncoder()
    data["label"] = label_encoder_crop.fit_transform(data["label"])
    data["Fertilizer"] = label_encoder_fertilizer.fit_transform(data["Fertilizer"])

    # Features and targets
    feature_cols = ["N", "P", "K", "rainfall", "ph"]
    X = data[feature_cols]
    y_crop = data["label"]
    y_fertilizer = data["Fertilizer"]

    # Single split for all targets (keeps rows aligned)
    X_train, X_test, y_crop_train, y_crop_test, y_fertilizer_train, y_fertilizer_test = train_test_split(
        X,
        y_crop,
        y_fertilizer,
        test_size=0.2,
        random_state=42
    )

    # Base models
    rf_model = RandomForestClassifier(random_state=42)
    gb_model = GradientBoostingClassifier(random_state=42)
    lr_model = LogisticRegression(max_iter=1000, random_state=42)

    # VotingClassifier for crop
    crop_model = VotingClassifier(
        estimators=[
            ("RandomForest", rf_model),
            ("GradientBoosting", gb_model),
            ("LogisticRegression", lr_model),
        ],
        voting="soft"
    )
    crop_model.fit(X_train, y_crop_train)

    # VotingClassifier for fertilizer (new clones will be created internally)
    fertilizer_model = VotingClassifier(
        estimators=[
            ("RandomForest", RandomForestClassifier(random_state=42)),
            ("GradientBoosting", GradientBoostingClassifier(random_state=42)),
            ("LogisticRegression", LogisticRegression(max_iter=1000, random_state=42)),
        ],
        voting="soft"
    )
    fertilizer_model.fit(X_train, y_fertilizer_train)

    return crop_model, fertilizer_model, label_encoder_crop, label_encoder_fertilizer


# Train once on import (you can move this into a Django-ready init if needed)
CROP_MODEL, FERTILIZER_MODEL, CROP_ENCODER, FERTILIZER_ENCODER = load_and_train_models()


def predict_crop_and_fertilizer(n, p, k, rainfall, ph):
    """Predict the crop and fertilizer based on input parameters."""
    # Ensure 2D array for sklearn
    input_features = np.array([[n, p, k, rainfall, ph]], dtype=float)

    # Overall ensemble predictions
    crop_proba = CROP_MODEL.predict_proba(input_features)[0]
    fert_proba = FERTILIZER_MODEL.predict_proba(input_features)[0]

    # Index of the most probable class
    best_crop_idx = int(np.argmax(crop_proba))
    best_fert_idx = int(np.argmax(fert_proba))

    # Find which base model contributed the highest probability
    crop_contributions = {}
    for name, model in CROP_MODEL.named_estimators_.items():
        model_proba = model.predict_proba(input_features)[0][best_crop_idx]
        crop_contributions[name] = float(model_proba)
    strongest_crop_model = max(crop_contributions, key=crop_contributions.get)

    fertilizer_contributions = {}
    for name, model in FERTILIZER_MODEL.named_estimators_.items():
        model_proba = model.predict_proba(input_features)[0][best_fert_idx]
        fertilizer_contributions[name] = float(model_proba)
    strongest_fertilizer_model = max(fertilizer_contributions, key=fertilizer_contributions.get)

    # Final predicted class from the ensemble
    crop_class_encoded = CROP_MODEL.predict(input_features)[0]
    fert_class_encoded = FERTILIZER_MODEL.predict(input_features)[0]

    # Decode to original labels
    predicted_crop = CROP_ENCODER.inverse_transform([crop_class_encoded])[0]
    predicted_fertilizer = FERTILIZER_ENCODER.inverse_transform([fert_class_encoded])[0]

    return {
        "predicted_crop": predicted_crop,
        "strongest_crop_model": strongest_crop_model,
        "predicted_fertilizer": predicted_fertilizer,
        "strongest_fertilizer_model": strongest_fertilizer_model,
    }
