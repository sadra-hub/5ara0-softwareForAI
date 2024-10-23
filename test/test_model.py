import os
import tensorflow as tf
from tensorflow import keras
from model import build_model, load_model

TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")

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
