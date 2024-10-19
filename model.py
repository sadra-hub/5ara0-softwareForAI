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
    model : keras Model
        Model definition (untrained).
    """
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)),  # Assuming grayscale images
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(3, activation='softmax')  # Assuming 3 classes: J, Q, K
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    return model


def train_model(model, n_validation, write_to_file=False):
    """
    Fit the model on the training data set.

    Arguments
    ---------
    model : keras Model
        Model structure to fit, as defined by build_model().
    n_validation : int
        Number of training examples used for cross-validation.
    write_to_file : bool
        Write model to file; can later be loaded through load_model().
    
    Returns
    -------
    model : keras Model
        The trained model.
    """

    training_images, training_labels, validation_images, validation_labels = \
        load_data_set(TRAINING_IMAGE_DIR, n_validation)
        
    model.fit(training_images, training_labels, validation_data=(validation_images, validation_labels), epochs=10)

    if write_to_file:
        model.save('card_model.h5')  # Save the model to a file

    return model


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
