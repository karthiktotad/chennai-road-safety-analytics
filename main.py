"""
Master Execution Pipeline for Chennai Road Accident Research.
Allows modular or end-to-end execution of all pipeline stages.
"""

import sys
import argparse
import logging
import subprocess

from src.data_collection.run_collection import run_all_collections
from src.preprocessing.data_auditor import run_full_data_audit
from src.preprocessing.cleaner import run_all_preprocessing
from src.preprocessing.spatial_cleaner import run_all_spatial_preprocessing
from src.preprocessing.integrator import build_integrated_modeling_dataset
from src.statistical_analysis.eda import ChennaiAccidentEDA
from src.statistical_analysis.tests import StatisticalHypothesisTester
from src.feature_engineering.features import ChennaiFeatureEngineer
from src.modeling.train import SeverityModelTrainer
from src.evaluation.metrics import ModelEvaluator
from src.geospatial.hotspots import ChennaiGeospatialAnalyzer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline(stage="all"):
    logger.info(f"=== Starting Pipeline Execution: Stage='{stage}' ===")

    if stage in ["collect", "all"]:
        logger.info("\n>>> STAGE 2: Automated Data Ingestion")
        run_all_collections()

    if stage in ["audit", "all"]:
        logger.info("\n>>> STAGE 3: Data Inspection & Audit")
        run_full_data_audit()

    if stage in ["preprocess", "all"]:
        logger.info("\n>>> STAGE 4: Cleaning & Spatial Integration")
        run_all_preprocessing()
        run_all_spatial_preprocessing()
        build_integrated_modeling_dataset()

    if stage in ["eda", "all"]:
        logger.info("\n>>> STAGE 5: Exploratory Data Analysis")
        eda = ChennaiAccidentEDA()
        eda.generate_all_visualizations()

    if stage in ["stats", "all"]:
        logger.info("\n>>> STAGE 6: Statistical Hypothesis Testing & Regression")
        tester = StatisticalHypothesisTester()
        tester.run_all_statistical_analyses()

    if stage in ["features", "all"]:
        logger.info("\n>>> STAGE 7: Feature Engineering")
        fe = ChennaiFeatureEngineer()
        fe.build_features()

    if stage in ["train", "all"]:
        logger.info("\n>>> STAGE 8 & 9: Model Training, Evaluation, and SHAP")
        trainer = SeverityModelTrainer()
        trainer.train_and_save_all_models()
        evaluator = ModelEvaluator()
        evaluator.run_full_evaluation()

    if stage in ["geo", "all"]:
        logger.info("\n>>> STAGE 10: Geospatial Hotspot Identification")
        geo = ChennaiGeospatialAnalyzer()
        geo.run_all_geospatial_analysis()

    logger.info(f"\n=== Pipeline Execution Completed Successfully for Stage='{stage}' ===")


def main():
    parser = argparse.ArgumentParser(description="Chennai Road Accident Research Master Pipeline")
    parser.add_argument("--stage", type=str, default="all",
                        choices=["collect", "audit", "preprocess", "eda", "stats", "features", "train", "geo", "all", "app"],
                        help="Specific pipeline stage to execute")
    args = parser.parse_args()

    if args.stage == "app":
        logger.info("Launching Streamlit Research Dashboard...")
        subprocess.run(["streamlit", "run", "app.py"])
    else:
        run_pipeline(args.stage)


if __name__ == "__main__":
    main()

