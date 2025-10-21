import os
import numpy as np
from tensorflow import keras
from data_sets import IMAGE_SIZE, TEST_IMAGE_DIR
from model import build_model, load_model, evaluate_model, identify

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
        try:
            load_model()  # This should raise the FileNotFoundError if file doesn't exist and validate the model if the file does exist
        except FileNotFoundError as e:
            assert str(e) == "Model file 'card_model.h5' does not exist."
        else:
            """Since file exists, load and validate the saved model"""
            model = load_model()

            # Check if the model is a valid Keras model
            assert isinstance(model, keras.Model)

            # Optionally, check if the model has the expected structure
            # Assuming the original model has specific layers like Conv2D, MaxPooling2D, etc.
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


    def test_identify(self, mock_model, mocker):
        """Test the identify function."""
        # Mocking the raw image input
        raw_image = np.random.rand(*RAW_IMAGE_SHAPE)

        # Mocking the normalization process
        normalized_image = np.random.rand(*RAW_IMAGE_SHAPE)  # Normalized image
        mocker.patch('model.normalize_image', return_value=normalized_image)

        # Mocking the prediction process
        mock_model.predict.return_value = np.array([[0.1, 0.8, 0.1]])  # Mock predictions (Q)

        # Call the function under test
        rank = identify(raw_image, mock_model)

        # Assertions
        assert rank == 'Q'  # Based on the mock prediction
        
        # Use np.array_equal for array comparison
        expected_input = np.expand_dims(normalized_image, axis=0)
        mock_model.predict.assert_called_once()
        
        # Check if the actual call arguments match the expected input
        actual_call_args = mock_model.predict.call_args[0][0]  # Extract the first argument from the call
        assert np.array_equal(actual_call_args, expected_input), "The model was not called with the expected input."
