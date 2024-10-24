import pytest
from PIL import Image  
from client.state import ClientGameRoundState

class TestClientGameRoundState:
    def test_initial_state(self, game_round):
        """Test the initial state of a new game round."""
        assert game_round.get_coordinator_id() == "coordinator_1"
        assert game_round.get_round_id() == 1
        assert game_round.get_card() is None
        assert game_round.get_card_image() is None
        assert game_round.get_turn_order() is None
        assert game_round.get_moves_history() == []
        assert game_round.get_available_actions() == []
        assert game_round.get_outcome() is None
        assert game_round.get_cards() is None

    def test_set_card(self, game_round):
        """Test setting and getting the card."""
        game_round.set_card("K")
        assert game_round.get_card() == "K"

    def test_set_card_image(self, game_round):
        """Test setting and getting the card image."""
        # Mocking an image using PIL
        image = Image.new("RGB", (60, 30), color="red")
        game_round.set_card_image(image)
        assert game_round.get_card_image() == image

    def test_set_turn_order(self, game_round):
        """Test setting and getting the turn order."""
        game_round.set_turn_order(1)
        assert game_round.get_turn_order() == 1

    def test_add_move_history(self, game_round):
        """Test adding moves to the history."""
        game_round.add_move_history("BET")
        assert game_round.get_moves_history() == ["BET"]

    def test_set_moves_history(self, game_round):
        """Test setting the entire move history."""
        moves = ["BET", "CALL"]
        game_round.set_moves_history(moves)
        assert game_round.get_moves_history() == moves

    def test_set_available_actions(self, game_round):
        """Test setting available actions."""
        actions = ["CHECK", "FOLD"]
        game_round.set_available_actions(actions)
        assert game_round.get_available_actions() == actions

    def test_set_outcome(self, game_round):
        """Test setting and getting the outcome."""
        game_round.set_outcome(50)
        assert game_round.get_outcome() == 50

    def test_set_cards(self, game_round):
        """Test setting and getting the showdown cards."""
        game_round.set_cards("KJ")
        assert game_round.get_cards() == "KJ"

    def test_is_ended(self, game_round):
        """Test the is_ended method."""
        # Game should not be ended initially
        assert not game_round.is_ended()
        # Set an outcome, indicating the round has ended
        game_round.set_outcome(-20)
        assert game_round.is_ended()

    # Valid Test Cases
    @pytest.mark.parametrize("card", ["J", "Q", "K", "?"])
    def test_set_valid_card(self, game_round, card):
        """Test setting valid cards."""
        game_round.set_card(card)
        assert game_round.get_card() == card

    @pytest.mark.parametrize("order", [1, 2])
    def test_valid_turn_order(self, game_round, order):
        """Test setting valid turn orders."""
        game_round.set_turn_order(order)
        assert game_round.get_turn_order() == order

    @pytest.mark.parametrize("move", ["BET", "CALL", "CHECK", "FOLD"])
    def test_valid_moves_history(self, game_round, move):
        """Test adding valid moves to the history."""
        game_round.add_move_history(move)
        assert move in game_round.get_moves_history()

    def test_valid_available_actions(self, game_round):
        """Test setting valid available actions."""
        valid_actions = ["BET", "CHECK", "FOLD", "CALL"]
        game_round.set_available_actions(valid_actions)
        assert game_round.get_available_actions() == valid_actions