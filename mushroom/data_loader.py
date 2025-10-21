import os

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Data loader marks the root directory
DATA_PATH = os.path.join(ROOT_DIR, "datasets")

# Features used for prediction
FEATURES = {
    "cap-diameter": "number in cm",
    "cap-shape": "bell=b, conical=c, convex=x, flat=f, sunken=s, spherical=p, others=o",
    "cap-surface": "fibrous=i, grooves=g, scaly=y, smooth=s, shiny=h, leathery=l, silky=k, sticky=t, wrinkled=w, fleshy=e",
    "cap-color": "brown=n, buff=b, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y, blue=l, orange=o, black=k",
    "does-bruise-or-bleed": "bruises-or-bleeding=t, no=f",
    "gill-attachment": "adnate=a, adnexed=x, decurrent=d, free=e, sinuate=s, pores=p, none=f, unknown=?",
    "gill-spacing": "close=c, distant=d, none=f",
    "gill-color": "brown=n, buff=b, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y, blue=l, orange=o, black=k, none=f",
    "stem-height": "number in cm",
    "stem-width": "number in mm",
    "stem-root": "bulbous=b, swollen=s, club=c, cup=u, equal=e, rhizomorphs=z, rooted=r",
    "stem-surface": "fibrous=i, grooves=g, scaly=y, smooth=s, shiny=h, leathery=l, silky=k, sticky=t, wrinkled=w, fleshy=e, none=f",
    "stem-color": "brown=n, buff=b, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y, blue=l, orange=o, black=k, none=f",
    "veil-type": "partial=p, universal=u",
    "veil-color": "brown=n, buff=b, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y, blue=l, orange=o, black=k, none=f",
    "has-ring": "ring=t, none=f",
    "ring-type": "cobwebby=c, evanescent=e, flaring=r, grooved=g, large=l, pendant=p, sheathing=s, zone=z, scaly=y, movable=m, none=f, unknown=?",
    "spore-print-color": "brown=n, buff=b, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y, blue=l, orange=o, black=k",
    "habitat": "grasses=g, leaves=l, meadows=m, paths=p, heaths=h, urban=u, waste=w, woods=d",
    "season": "spring=s, summer=u, autumn=a, winter=w",
}

# Numerical features
NUMERICAL = ["cap-diameter", "stem-height", "stem-width"]

# Quantity that is predicted
TARGET = "edible"


def query_input_data(features=FEATURES, num_features=NUMERICAL):
    """
    Query user for input data.

    :param features: dictionary of valid features with additional info;
    :param num_features: list of numerical features;
    :return: a DataFrame with sanitized inputs.
    """

    # Initialize an empty dictionary of data entries
    input_data = {}
    for feature in features:
        input_data[feature] = []

    # Append sanitized values to dictionary
    for feature in features:
        raw_value = input(f"{feature} ({features[feature]}): ")  # Request input
        (_, sanitized_value) = sanitize_data_entry(
            feature, raw_value, features, num_features
        )
        input_data[feature].append(sanitized_value)  # Update dictionary with entry

    return pd.DataFrame(input_data)  # Convert entries to DataFrame


def sanitize_data_entry(feature, raw_value, features=FEATURES, num_features=NUMERICAL):
    """
    Sanitize the data entry by checking if the feature is valid, handling empty input, and converting raw values to the appropriate data type if necessary.

    Args:
        feature (str): The feature to sanitize.
        raw_value (str): The raw value of the feature.
        features (list): List of valid features (default is FEATURES).
        num_features (list): List of numerical features (default is NUMERICAL).

    Returns:
        tuple: A tuple containing the sanitized feature and its corresponding value.
    """

    # <ASSIGNMENT 2.3: Write the data sanitation functionality>

    # Check if the feature is valid
    if feature not in features:
        raise ValueError(f"🚫 Invalid feature: {feature}")

    # Handle empty input
    if raw_value == "":
        return (feature, float("nan"))

    # Check if the feature is numerical
    if feature in num_features:
        try:
            # Attempt to convert the raw value to a float
            sanitized_value = float(raw_value)
        except ValueError:
            raise ValueError(
                f"🚫 Non-numeric value provided for numerical feature: {raw_value}"
            )
    else:
        # Categorical features should just return the raw value as a string
        sanitized_value = raw_value

    return feature, sanitized_value


def load_data(data_path=DATA_PATH):
    """
    Load dataset in a DataFrame.

    :param data_path: root folder of data file;
    :return: DataFrame with raw dataset.
    """

    csv_path = os.path.join(data_path, "dataset.csv")

    return pd.read_csv(csv_path, delimiter=";")


def split_train_test(dataset):
    """
    Split the dataset into a train and test set.

    Args:
        dataset (pd.DataFrame): The input dataset to be split.

    Returns:
        list: A list containing the train and test sets as DataFrames.

    Raises:
        ValueError: If the input dataset is not a pandas DataFrame.
    """

    # <ASSIGNMENT 3.1: Split the dataset in a train and test set>
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError("Input dataset must be a pandas DataFrame.")

    # Split the dataset into train and test sets with an 80/20 ratio
    train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=42)

    # Return as a list of DataFrames
    dataset = [train_set, test_set]

    return dataset
