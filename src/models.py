"""Model definitions for Sklearn, XGBoost, and PyTorch."""

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor

from src.utils import get_logger

logger = get_logger(__name__)


class MLP(nn.Module):
    """Simple Multi-Layer Perceptron for Tabular Data."""

    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int = 64):
        super(MLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, output_dim),
        )

    def forward(self, x):
        return self.network(x)


class ModelWrapper:
    """Unified interface for different models."""

    def __init__(self, model_name: str, task: str, input_dim: int):
        self.model_name = model_name
        self.task = task
        self.model = self._build_model(input_dim)

    def _build_model(self, input_dim: int):
        if self.model_name == "sklearn":
            if self.task == "classification":
                return RandomForestClassifier(random_state=42, n_estimators=100)
            else:
                return RandomForestRegressor(random_state=42, n_estimators=100)

        elif self.model_name == "xgboost":
            if self.task == "classification":
                return XGBClassifier(
                    random_state=42,
                    n_estimators=100,
                    use_label_encoder=False,
                )
            else:
                return XGBRegressor(random_state=42, n_estimators=100)

        elif self.model_name == "pytorch":
            output_dim = 1 if self.task == "regression" else 2
            return MLP(input_dim=input_dim, output_dim=output_dim)

        else:
            raise ValueError(f"Model {self.model_name} not supported.")

    def fit(
        self,
        X_train,
        y_train,
        X_val,
        y_val,
        epochs: int,
        lr: float,
        device: str,
    ):
        if self.model_name == "pytorch":
            return self._fit_torch(X_train, y_train, X_val, y_val, epochs, lr, device)
        else:
            return self._fit_sklearn(X_train, y_train)

    def _fit_sklearn(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return None

    def _fit_torch(
        self,
        X_train,
        y_train,
        X_val,
        y_val,
        epochs: int,
        lr: float,
        device: str,
    ):
        criterion = nn.MSELoss() if self.task == "regression" else nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.model.to(device)

        history = {"train_loss": [], "val_loss": []}
        train_tensor = torch.FloatTensor(X_train).to(device)
        y_train_tensor = torch.FloatTensor(y_train).to(device)
        val_tensor = torch.FloatTensor(X_val).to(device)
        y_val_tensor = torch.FloatTensor(y_val).to(device)

        if self.task == "classification":
            y_train_tensor = y_train_tensor.long()
            y_val_tensor = y_val_tensor.long()

        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            outputs = self.model(train_tensor)

            if self.task == "regression":
                outputs = outputs.squeeze()
                y_train_tensor = y_train_tensor.squeeze()

            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()

            self.model.eval()
            with torch.no_grad():
                val_outputs = self.model(val_tensor)
                if self.task == "regression":
                    val_outputs = val_outputs.squeeze()
                    y_val_tensor = y_val_tensor.squeeze()
                val_loss = criterion(val_outputs, y_val_tensor)

            history["train_loss"].append(loss.item())
            history["val_loss"].append(val_loss.item())

            if (epoch + 1) % 10 == 0:
                logger.info(
                    f"Epoch {epoch+1}/{epochs}, "
                    f"Train Loss: {loss.item():.4f}, "
                    f"Val Loss: {val_loss.item():.4f}"
                )

        return history

    def predict(self, X):
        if self.model_name == "pytorch":
            self.model.eval()
            with torch.no_grad():
                preds = self.model(torch.FloatTensor(X))
                if self.task == "regression":
                    return preds.squeeze().numpy()
                else:
                    return torch.argmax(preds, dim=1).numpy()
        else:
            return self.model.predict(X)
