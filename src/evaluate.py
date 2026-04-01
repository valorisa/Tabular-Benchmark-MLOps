"""Evaluation metrics for classification and regression."""

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score

from src.utils import get_logger

logger = get_logger(__name__)


def evaluate_model(y_true, y_pred, task: str):
    """Calculate metrics based on task type."""
    metrics = {}

    if task == "classification":
        metrics["accuracy"] = accuracy_score(y_true, y_pred)
        metrics["f1"] = f1_score(y_true, y_pred, average="weighted")
        logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"F1 Score: {metrics['f1']:.4f}")

    elif task == "regression":
        metrics["rmse"] = np.sqrt(mean_squared_error(y_true, y_pred))
        metrics["r2"] = r2_score(y_true, y_pred)
        logger.info(f"RMSE: {metrics['rmse']:.4f}")
        logger.info(f"R2: {metrics['r2']:.4f}")

    else:
        raise ValueError(f"Task {task} not supported.")

    return metrics
