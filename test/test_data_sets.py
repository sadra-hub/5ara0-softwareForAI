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

    def test_load_data_set(self):
        """
        Test if the images are loaded and divided into training and validation sets.
        """
        # Check for the case when n_validation = 0
        training_images, training_labels, validation_images, validation_labels = load_data_set(TRAINING_IMAGE_TEST_DIR) # use training data in test directory to split into training/validation sets
        # Check validation set information when n_validation = 0
        assert validation_labels == None and validation_features == None
        # Check training set information when n_validation = 0
        number_of_training_labels = len(training_labels)
        number_of_training_images = len(training_images)

        assert number_of_training_labels == NUM_CLASSES and number_of_training_images == NUM_CLASSES

        # Now in the case that n_validation = 1
        n_validation = 1
        diff = NUM_CLASSES - n_validation

        training_images, training_labels, validation_images, validation_labels = load_data_set(TEST_IMAGE_TEST_DIR, n_validation)

        # Check if the total number of images is split correctly into training and validation sets
        assert len(training_images) + len(validation_images) == NUM_CLASSES, "Total images should match the split between training and validation."

        # Check if the number of validation images matches n_validation
        assert len(validation_images) == n_validation, f"Validation set should have {n_validation} images."

        # Check if the number of training images is correct
        assert len(training_images) == diff, f"Training set should have {diff} images."

        # Test if labels are correctly generated 
        assert training_labels.shape[1] == diff
        assert validation_labels.shape[1] == n_validation

