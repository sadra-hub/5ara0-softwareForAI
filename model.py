import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model as keras_load_model # type: ignore
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
    model : keras Model
        Previously trained model.
    """
    model_path = "card_model.h5"

    # Check if the file exists, raise a FileNotFoundError if it doesn't
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' does not exist.")

    # Load the model
    return keras.models.load_model(model_path)

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
    score = model.evaluate(test_images, test_labels)
    return score[0]  # Return the loss value

def identify(raw_image, model):
    """
    Use model to classify a single card image.

    Arguments
    ---------
    raw_image : Image
        Raw image to classify.
    model : keras Model
        Trained model.

    Returns
    -------
    rank : str in ['J', 'Q', 'K']
        Estimated card rank.
    """

    image = normalize_image(raw_image)
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    prediction = model.predict(image)
    rank_index = np.argmax(prediction)

    # Assuming 0: J, 1: Q, 2: K
    ranks = ['J', 'Q', 'K']
    return ranks[rank_index]
