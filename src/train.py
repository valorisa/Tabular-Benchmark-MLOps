"""Training pipeline with W&B logging."""

import wandb
from src.evaluate import evaluate_model
from src.models import ModelWrapper
from src.utils import get_logger

logger = get_logger(__name__)


def train_pipeline(
    model_name: str,
    task: str,
    X_train,
    X_test,
    y_train,
    y_test,
    config,
    device,
):
    """Full training and evaluation pipeline."""
    input_dim = X_train.shape[1]
    model_wrapper = ModelWrapper(model_name, task, input_dim)

    run_name = f"{task}_{model_name}"
    wandb.init(
        project=config["wandb_project"],
        entity=config.get("wandb_entity"),
        name=run_name,
        config={
            "model": model_name,
            "task": task,
            "epochs": config["epochs"],
            "lr": config["learning_rate"],
            "batch_size": config["batch_size"],
            "seed": config["seed"],
        },
    )

    logger.info(f"Starting training for {model_name} on {task}")

    history = model_wrapper.fit(
        X_train,
        y_train,
        X_test,
        y_test,
        epochs=config["epochs"],
        lr=config["learning_rate"],
        device=device,
    )

    if history:
        for epoch, (t_loss, v_loss) in enumerate(
            zip(history["train_loss"], history["val_loss"])
        ):
            wandb.log({"train_loss": t_loss, "val_loss": v_loss, "epoch": epoch})

    y_pred = model_wrapper.predict(X_test)
    metrics = evaluate_model(y_test, y_pred, task)

    wandb.log(metrics)
    wandb.finish()

    logger.info(f"Training completed for {model_name}. Metrics logged to W&B.")
    return metrics
