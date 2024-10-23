from data_sets import *
import numpy as np
import pytest
import random
from PIL import Image, ImageDraw, ImageFont
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")


class TestDataSets:
    # You don't need to test generate_data_set() (that will take too much time to run)

    def test_normalize_image(self, image):
        """
        Test whether the behaviour of normalize_image() returns a properly normalized image.
        """
        # Call the function to normalize the provided test image
        normalized_img = normalize_image(image)

        # Ensure the image shape and data type are correct after normalization
        assert normalized_img.dtype == np.float32, "Expected data type float32 for the image"
        assert normalized_img.shape == (IMAGE_SIZE, IMAGE_SIZE), "Image shape mismatch"

        # Check if the normalized image values are constrained between 0 and 1
        assert normalized_img.max() <= 1, "Maximum value exceeds 1"
        assert normalized_img.min() >= 0, "Minimum value is below 0"

    def test_generate_noisy_image(self):

        """
        Test if generate_noisy_image gives correct output
        """
    
        #test if the image is generated has the correct shape
        rank = random.choice(LABELS)
        img = generate_noisy_image(rank, 0.6)

        assert(img.size) == (IMAGE_SIZE, IMAGE_SIZE)

        #test for rank must be in LABELS for upper/lower case
        assert pytest.raises(ValueError, generate_noisy_image, "ab", 0.5)
        assert pytest.raises(ValueError, generate_noisy_image, "AB", 0.5)

        #test for noise level must be between 0 and 1
        assert pytest.raises(ValueError, generate_noisy_image, rank , -0.1) 
        assert pytest.raises(ValueError, generate_noisy_image, rank , 1.1)


