"""
Machine Learning Model Training Pipeline.
Develops, trains, and serializes four supervised learning models for accident severity classification:
1. Logistic Regression (Interpretable Statistical Baseline)
2. Decision Tree Classifier (Non-linear Rule Baseline)
3. Random Forest Classifier (Ensemble Bagging)
4. XGBoost Classifier (Gradient Boosting)

Enforces strict train-test separation to eliminate data leakage.
"""

import json
import logging
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from config.settings import (
    PROCESSED_DATA_DIR, MODELS_DIR, RANDOM_SEED, TEST_SIZE, TARGET_COLUMN
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class SeverityModelTrainer:
    """Orchestrates model development and serialized artifact storage."""

    def __init__(self):
        self.data_path = PROCESSED_DATA_DIR / "chennai_feature_matrix.csv"
        self.meta_path = MODELS_DIR / "feature_metadata.json"
        self.models_dir = MODELS_DIR
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def load_data_and_schema(self):
        df = pd.read_csv(self.data_path)
        with open(self.meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        num_cols = metadata["numerical_features"]
        bin_cols = metadata["binary_features"]
        cat_cols = metadata["categorical_features"]
        feature_cols = num_cols + bin_cols + cat_cols

        X = df[feature_cols]
        y = df[TARGET_COLUMN]

        logger.info(f"Loaded dataset: X shape = {X.shape}, y severe distribution = {y.value_counts().to_dict()}")
        return X, y, num_cols, bin_cols, cat_cols

    def build_preprocessor(self, num_cols, bin_cols, cat_cols):
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), num_cols),
                ("bin", "passthrough", bin_cols),
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), cat_cols)
            ]
        )
        return preprocessor

    def train_and_save_all_models(self):
        X, y, num_cols, bin_cols, cat_cols = self.load_data_and_schema()

        # Stratified Train-Test Split (80% Train, 20% Test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
        )
        logger.info(f"Stratified Split: Train N={len(X_train)} ({y_train.mean():.1%} severe), Test N={len(X_test)} ({y_test.mean():.1%} severe)")

        # Save test partition for standalone evaluation
        test_df = X_test.copy()
        test_df[TARGET_COLUMN] = y_test.values
        test_df.to_csv(PROCESSED_DATA_DIR / "holdout_test_set.csv", index=False)

        preprocessor = self.build_preprocessor(num_cols, bin_cols, cat_cols)

        # Fit preprocessor strictly on training data
        preprocessor.fit(X_train)
        joblib.dump(preprocessor, self.models_dir / "preprocessor.joblib")
        logger.info("Saved preprocessor to models/preprocessor.joblib")

        # Class balance ratio for XGBoost (num_negative / num_positive)
        n_pos = (y_train == 1).sum()
        n_neg = (y_train == 0).sum()
        scale_pos_weight = n_neg / n_pos if n_pos > 0 else 1.0

        models = {
            "Logistic Regression": LogisticRegression(
                C=1.0, max_iter=1000, class_weight="balanced", random_state=RANDOM_SEED
            ),
            "Decision Tree": DecisionTreeClassifier(
                max_depth=6, min_samples_split=20, min_samples_leaf=10,
                class_weight="balanced", random_state=RANDOM_SEED
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=150, max_depth=8, min_samples_split=15,
                class_weight="balanced", random_state=RANDOM_SEED, n_jobs=-1
            ),
            "XGBoost": XGBClassifier(
                n_estimators=150, max_depth=5, learning_rate=0.05,
                scale_pos_weight=scale_pos_weight, eval_metric="logloss",
                random_state=RANDOM_SEED
            )
        }

        fitted_pipelines = {}
        predictions = {}

        for name, clf in models.items():
            logger.info(f"Training {name} pipeline...")
            pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("classifier", clf)
            ])
            pipeline.fit(X_train, y_train)

            # Save serialized pipeline
            slug = name.lower().replace(" ", "_")
            model_file = self.models_dir / f"{slug}_pipeline.joblib"
            joblib.dump(pipeline, model_file)
            logger.info(f"Saved {name} model to {model_file}")

            # Predict on test split
            y_pred = pipeline.predict(X_test)
            y_proba = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred

            fitted_pipelines[name] = pipeline
            predictions[name] = {
                "y_pred": y_pred,
                "y_proba": y_proba
            }

        # Save test predictions for evaluation
        eval_payload = {
            "y_test": y_test.values.tolist(),
            "predictions": {name: {
                "y_pred": p["y_pred"].tolist(),
                "y_proba": p["y_proba"].tolist()
            } for name, p in predictions.items()}
        }
        with open(self.models_dir / "test_predictions.json", "w", encoding="utf-8") as f:
            json.dump(eval_payload, f)

        logger.info("All 4 models successfully trained, evaluated on holdout test set, and serialized.")
        return fitted_pipelines, predictions, X_test, y_test


if __name__ == "__main__":
    trainer = SeverityModelTrainer()
    trainer.train_and_save_all_models()

