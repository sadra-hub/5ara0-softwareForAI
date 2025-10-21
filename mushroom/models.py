import os

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, cross_val_score

from data_loader import ROOT_DIR

MODEL_PATH = os.path.join(ROOT_DIR, "models")


def build_model():
    """
    Builds a Random Forest Classifier model with optimal parameters.

    Returns:
        RandomForestClassifier: A Random Forest Classifier model with the following parameters:
            - n_estimators: Number of trees
            - max_depth: Maximum depth of each tree
            - min_samples_split: Minimum samples required to split an internal node
            - min_samples_leaf: Minimum samples required at each leaf node
            - random_state: For reproducibility
    """

    # <ASSIGNMENT 3.5: Define a suitable model>
    # Initialize the Random Forest Classifier with optimal parameters, according to finetune_model()
    model = RandomForestClassifier(
        n_estimators=50,  # Number of trees
        max_depth=None,  # Maximum depth of each tree
        min_samples_split=2,  # Minimum samples required to split an internal node
        min_samples_leaf=1,  # Minimum samples required at each leaf node
        random_state=42,
    )  # For reproducibility

    return model


def cross_validate_model(model, X_train, y_train):
    """
    Perform a 5-fold cross-validation and report a suitable metric.

    Args:
        model: The machine learning model to be cross-validated.
        X_train: The training data features.
        y_train: The training data labels.

    Returns:
        Array of scores obtained from the cross-validation.
    """

    # <ASSIGNMENT 3.6: Perform a 5-fold cross-validation and report a suitable metric>
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")

    return scores


def train_model(model, X_train, y_train):
    """
    Train a model on the training data.

    :param X_train: pre-processed training data (numpy array)
    :param y_train: pre-processed targets for training (numpy array)
    :return: fitted model
    """

    model.fit(X_train, y_train)

    return model


def save_model(model, model_path=MODEL_PATH):
    """
    Write model to file (note, model.pkl is not committed to git).

    :param model: model object
    :param model_path: path to model (string)
    :return: model object
    """

    os.makedirs(model_path, exist_ok=True)
    model_file = os.path.join(model_path, "model.pkl")
    joblib.dump(model, model_file)

    return model


def finetune_model(model, X_train, y_train):
    """
    Use a grid search to finetune model parameters.

    Args:
        model: The machine learning model to be fine-tuned.
        X_train: The training data.
        y_train: The target labels.

    Returns:
        dict: The best parameters found by the grid search.
    """

    # <ASSIGNMENT 3.8: Use a grid search to finetune model parameters>
    # Define the parameter grid
    param_grid = {
        "n_estimators": [50, 100, 200],  # Number of trees in the forest
        "max_depth": [None, 10, 20, 30],  # Maximum depth of the tree
        "min_samples_split": [
            2,
            5,
            10,
        ],  # Minimum number of samples required to split an internal node
        "min_samples_leaf": [
            1,
            2,
            4,
        ],  # Minimum number of samples required to be at a leaf node
    }

    # Initialize GridSearchCV
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring="accuracy",
        cv=5,
        verbose=1,
        n_jobs=-1,
    )

    # Fit grid search
    grid_search.fit(X_train, y_train)

    return grid_search.best_params_


def evaluate_model(model, X_test, y_test):
    """
    Evaluate a pre-trained model on a test set.

    :param model: pre-trained model
    :param X_test: pre-processed testing data (numpy array)
    :param y_test: pre-processed targets for training (numpy array)
    :return: training and cross-validation RMSE values
    """

    y_predicted = model.predict(X_test)
    score = confusion_matrix(y_test, y_predicted)

    return score


def load_model(model_path=MODEL_PATH):
    """
    Load a model from file.

    :param model_path: path to model (string)
    :return: model object
    """
    model_file = os.path.join(model_path, "model.pkl")
    return joblib.load(model_file)


def predict(model, X):
    """
    Predict edibility from a pre-trained model.

    :param model: trained model
    :param X: sanitized and pre-processed data entry (numpy array)
    :return: predicted edibility
    """

    y_predicted = model.predict(X)

    return y_predicted
