import os
import pytest
from PIL import Image

from client.state import ClientGameState


TEST_DIR = os.path.join(os.path.abspath(__file__), "test")  # Mark the test root directory
TRAINING_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "training_images")
TEST_IMAGE_TEST_DIR = os.path.join(TEST_DIR, "data_sets", "test_images")


# Pytest loader requires a conftest with (empty) initialization
def __init__():
    pass


@pytest.fixture()
def image(request):
    return Image.open(os.path.join(TEST_IMAGE_TEST_DIR, "J_1.png"))

@pytest.fixture()
def client_game_state():
    # This fixture sets up a ClientGameState instance for tests
    return ClientGameState("coordinator_1", "player_1", 100)


# Define your own fixtures for testing here if you need them
