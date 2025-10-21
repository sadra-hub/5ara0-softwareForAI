import os

import numpy as np
import pandas as pd
import pytest

from data_loader import load_data, sanitize_data_entry

TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory


class TestDataLoader:
    """
    Unit tests for the TestDataLoader class.

    This class contains methods to test the functionality of data loading and sanitization processes 
    for a data processing application. It ensures that the data is loaded correctly from a specified 
    path and that the sanitization of data entries adheres to expected behaviors.

    Methods:
        test_load_data: Tests loading data from a specified path and verifies that the data is of 
                        the expected type and shape.
        test_sanitize_data_entry: Tests the sanitize_data_entry function with various input scenarios, 
                                  including valid and invalid cases for both numeric and categorical 
                                  features.
    """

    def test_load_data(self):
        """
        Test loading data from a specified path.

            This function tests the loading of data from a specified path using the load_data function.

            The function asserts that the loaded data is of type pd.DataFrame and has a shape of (30, 21).
        """
        raw_data = load_data(data_path=TEST_DIR)

        # <ASSIGNMENT 2.1: Find and fix the bug (in another file) to make both tests pass>
        assert isinstance(raw_data, pd.DataFrame), "Expected raw_data to be a pandas DataFrame."
        assert raw_data.shape == (30, 21), f"Expected shape (30, 21), but got {raw_data.shape}."

    def test_sanitize_data_entry(self):
        """
        Tests the sanitize_data_entry function with various scenarios.

        Valid modes of behavior:
        0. For a numeric feature, the input should be converted into a float.
        1. For a numeric feature, an empty input (""), should be interpreted as nan.
        2. For a categorical feature, an empty input (""), should also be interpreted as nan.
        3. For a categorical feature, the input should be interpreted as a string.

        Invalid modes of behavior:
        0. A numeric entry with a non-numeric input should raise a ValueError.
        1. An entry for which the queried feature is not within the list of valid features should raise a ValueError.
        """

        # Define feature names and descriptions for testing
        features = {
            "numeric_feature": "Description for a numeric feature",
            "categorical_feature": "Description for a categorical feature",
        }
        num_features = ["numeric_feature"]

        # <ASSIGNMENT 2.2: Write the five additional tests>

        # Valid modes of behavior
        # 0. For a numeric feature, the input should be converted into a float
        result = sanitize_data_entry("numeric_feature", "1", features, num_features)
        assert result == (
            "numeric_feature",
            1.0,
        )

        # 1. For a numeric feature, an empty input (""), should be interpreted as nan
        result = sanitize_data_entry("numeric_feature", "", features, num_features)
        # Using np.isnan() to see if the sanitized_value is equal to NaN.
        # Comparing NaN to NaN using '!=' results in False, as per IEEE 754 standards. [IGNORE PT018]
        assert result[0] == "numeric_feature" and np.isnan(result[1]), "❌ Expected nan for empty input (numeric_feature)"

        # 2. For a categorical feature, an empty input (""), should also be interpreted as nan
        result = sanitize_data_entry("categorical_feature", "", features, num_features)
        # Using np.isnan() to see if the sanitized_value is equal to NaN.
        # Comparing NaN to NaN using '!=' results in False, as per IEEE 754 standards. [IGNORE PT018]
        assert result[0] == "categorical_feature" and np.isnan(result[1]), "Expected nan for empty input (categorical_feature)"

        # 3. For a categorical feature, the input should be interpreted as a string
        assert sanitize_data_entry(
            "categorical_feature", "some_string", features, num_features
        ) == (
            "categorical_feature",
            "some_string",
        )

        # Invalid modes of behavior
        # 0. A numeric entry with a non-numeric input should raise a ValueError
        try:
            sanitize_data_entry(
                "numeric_feature", "non_numeric_value", features, num_features
            )
            pytest.fail("❌ Expected ValueError not raised")
        except ValueError:
            pass  # Test passes if ValueError is raised

        # 1. An entry for which the queried feature is not within the list of valid features should raise a ValueError
        try:
            sanitize_data_entry("invalid_feature", "1", features, num_features)
            pytest.fail("❌ Expected ValueError not raised")
        except ValueError:
            pass  # Test passes if ValueError is raised
