import os
import tensorflow as tf
import unittest
from tensorflow import keras
from model import build_model, load_model


TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")


class TestModel(unittest.TestCase):
    def test_build_model(self):
        model = build_model()

        # Check if it's a Sequential model
        self.assertIsInstance(model, keras.Sequential)

        # Check the number of layers in the model
        self.assertEqual(len(model.layers), 7)

        # Check the first layer is Conv2D with the right input shape
        self.assertIsInstance(model.layers[0], keras.layers.Conv2D)
        self.assertEqual(model.layers[0].input_shape, (None, 32, 32, 1))

        # Check if the model is compiled with the correct loss function
        self.assertEqual(model.loss, "sparse_categorical_crossentropy")

        # Check if the optimizer is Adam
        self.assertIsInstance(model.optimizer, keras.optimizers.Adam)

    def test_load_model(self):
        """Test if the model file exists before loading."""
        self.assertTrue(os.path.exists("card_model.h5"), "Model file does not exist")

        """Test if the model is loaded correctly from the file."""
        model = load_model()

        # Check if the model is a valid Keras model
        self.assertIsInstance(model, keras.Model)

        # Optionally, check if the model has the expected structure
        # Assuming the original model has specific layers like Conv2D, MaxPooling2D, etc.
        self.assertEqual(len(model.layers), 7)
        self.assertIsInstance(model.layers[0], keras.layers.Conv2D)
        self.assertIsInstance(model.layers[-1], keras.layers.Dense)


if __name__ == "__main__":
    unittest.main()