import os


TEST_DIR = os.path.dirname(os.path.abspath(__file__))  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")


class TestModel:
    # You don't need to test train_model() (that will take too much time to run)

    pass  # Replace with your own tests
