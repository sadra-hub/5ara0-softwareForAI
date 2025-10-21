import os

import joblib
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from data_loader import FEATURES, NUMERICAL, ROOT_DIR, TARGET

PIPELINE_PATH = os.path.join(ROOT_DIR, "pipelines")


def build_pipeline():
    """
    Builds a data preprocessing pipeline for numerical and categorical features.

    This function generates lists of numerical and categorical features based on the input FEATURES and NUMERICAL.
    It then creates separate pipelines for numerical and categorical features, including imputation and scaling for numerical features,
    and imputation and one-hot encoding for categorical features.

    Returns:
        ColumnTransformer: A scikit-learn ColumnTransformer object that preprocesses numerical and categorical features.
    """

    # Generate lists of numerical and categorical features
    cat_features = list(FEATURES.keys())
    num_features = NUMERICAL.copy()
    for num_feature in num_features:
        cat_features.remove(num_feature)

    # <ASSIGNMENT 3.3: Complete the numeric and categorical pipelines>
    # Define pipeline for numerical features
    num_pipeline = make_pipeline(
        SimpleImputer(strategy="median"),  # Impute missing values using median
        StandardScaler(),  # Scale to zero mean and unit variance
    )

    # Define pipeline for categorical features
    cat_pipeline = make_pipeline(
        SimpleImputer(
            strategy="constant", fill_value="missing"
        ),  # Impute missing values with 'missing'
        OneHotEncoder(
            handle_unknown="ignore"
        ),  # One-hot encode, ignoring unknown categories
    )

    pipeline = make_column_transformer(
        (num_pipeline, num_features), (cat_pipeline, cat_features)
    )

    return pipeline


def train_pipeline(pipeline, train_set):
    """
    Fit the pipeline on the training set

    :param pipeline: untrained pipeline
    :param train_set: dataset for fitting pipeline (DataFrame);
    :return: trained Pipeline
    """

    return pipeline.fit(train_set)


def save_pipeline(pipeline, pipeline_path=PIPELINE_PATH):
    """
    Write pipeline to file (note, *.pkl files are in .gitignore).

    :return: original pipeline
    """

    os.makedirs(pipeline_path, exist_ok=True)
    pipeline_file = os.path.join(pipeline_path, "pipeline.pkl")
    joblib.dump(pipeline, pipeline_file)

    return pipeline


def load_pipeline(pipeline_path=PIPELINE_PATH):
    """
    Load a pipeline from file.

    :param pipeline_path: path to trained pipeline (string);
    :return: pipeline object
    """

    pipeline_file = os.path.join(pipeline_path, "pipeline.pkl")

    return joblib.load(pipeline_file)


def apply_pipeline(pipeline, data_set):
    """
    Apply a trained pipeline to transform `data_set`.

    :param pipeline: trained pipeline
    :param data_set: datset for applying pipeline (DataFrame);
    :return: pre-processed dataset X and targets y (list of numpy arrays).
    """

    X = pipeline.transform(data_set)
    y = []
    if TARGET in data_set:
        y = data_set[TARGET]  # Extract target values if available

    return X, y
