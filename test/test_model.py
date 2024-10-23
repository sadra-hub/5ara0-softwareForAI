import os
import numpy as np
from tensorflow import keras
from data_sets import IMAGE_SIZE, TEST_IMAGE_DIR
from model import build_model, load_model, evaluate_model

TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")
RAW_IMAGE_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

class TestModel:

    def test_build_model(self):
        model = build_model()

        # Check if it's a Sequential model
        assert isinstance(model, keras.Sequential)

        # Check the number of layers in the model
        assert len(model.layers) == 7

        # Check the first layer is Conv2D with the right input shape
        assert isinstance(model.layers[0], keras.layers.Conv2D)
        
        # Check the input shape of the model
        assert model.input_shape == (None, 32, 32, 1)

        # Check if the model is compiled with the correct loss function
        assert model.loss == "sparse_categorical_crossentropy"

        # Check if the optimizer is Adam
        assert isinstance(model.optimizer, keras.optimizers.Adam)


    def test_load_model(self):
        """Test if the model file exists before loading."""
        assert os.path.exists("card_model.h5"), "Model file does not exist"

        """Test if the model is loaded correctly from the file."""
        model = load_model()

        # Check if the model is a valid Keras model
        assert isinstance(model, keras.Model)

        # Check if the model has the expected structure
        assert len(model.layers) == 7
        assert isinstance(model.layers[0], keras.layers.Conv2D)
        assert isinstance(model.layers[-1], keras.layers.Dense)

    def test_evaluate_model(self, mock_load_data_set, mock_model):
        """Test the evaluate_model function."""
        # Mocking the data set returned by load_data_set
        mock_test_images = np.random.rand(10, *RAW_IMAGE_SHAPE)  # 10 test images
        mock_test_labels = np.random.randint(0, 3, size=(10, 3))  # 10 test labels (one-hot encoded)

        # Set the return value for the mocked load_data_set function
        mock_load_data_set.return_value = (mock_test_images, mock_test_labels, None, None)

        # Mocking the evaluate method
        mock_model.evaluate.return_value = [0.25]  # Mocking the loss value returned by evaluate

        # Call the function under test
        score = evaluate_model(mock_model)

        # Assertions
        assert score == 0.25
        mock_load_data_set.assert_called_once_with(TEST_IMAGE_DIR)
        mock_model.evaluate.assert_called_once_with(mock_test_images, mock_test_labels)


