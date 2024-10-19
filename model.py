import numpy as np
import tensorflow as tf
from tensorflow import keras
from data_sets import normalize_image, load_data_set, TRAINING_IMAGE_DIR, TEST_IMAGE_DIR

layers = tf.keras.layers

def build_model():
    """
    Prepare the model.

    Returns
    -------
    model : model class from any toolbox you choose to use.
        Model definition (untrained).
    """

    pass


def train_model(model, n_validation, write_to_file=False):
    """
    Fit the model on the training data set.

    Arguments
    ---------
    model : model class
        Model structure to fit, as defined by build_model().
    n_validation : int
        Number of training examples used for cross-validation.
    write_to_file : bool
        Write model to file; can later be loaded through load_model().

    Returns
    -------
    model : model class
        The trained model.
    """

    training_images, training_labels, validation_images, validation_labels = \
        load_data_set(TRAINING_IMAGE_DIR, n_validation)


def load_model():
    """
    Load a model from file.

    Returns
    -------
    model : model class
        Previously trained model.
    """

    pass


def evaluate_model(model):
    """
    Evaluate model on the test set.

    Arguments
    ---------
    model : model class
        Trained model.

    Returns
    -------
    score : float
        A measure of model performance.
    """

    test_images, test_labels, _, _ = load_data_set(TEST_IMAGE_DIR)


def identify(raw_image, model):
    """
    Use model to classify a single card image.

    Arguments
    ---------
    raw_image : Image
        Raw image to classify.
    model : model class
        Trained model.

    Returns
    -------
    rank : str in ['J', 'Q', 'K']
        Estimated card rank.
    """

    image = normalize_image(raw_image)
