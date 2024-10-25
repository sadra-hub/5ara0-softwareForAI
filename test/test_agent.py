import pytest
from unittest.mock import MagicMock, patch, Mock
from agent import PokerAgent
from client.state import ClientGameState, ClientGameRoundState


class TestPokerAgent:
    @patch('agent.load_model')
    def test_agent_init(self, mock_load_model):
        """
        Test whether the agent correctly intialized.
        """
        # Create a mock model and set it as the return value for load_model.
        mock_model = Mock()
        mock_load_model.return_value = mock_model

        # Create a PokerAgent object, which will use the mocked `load_model`.
        agent = PokerAgent()

        gamestate = ClientGameState("coordinator_1", "player_1", 100)
        gameroundstate = ClientGameRoundState("coordinator_1", 1)

        # Assert that the model was loaded correctly and assigned to the agent.
        assert agent.model != None
        assert agent.model == mock_model

    @patch('agent.load_model')
    def test_make_action(self, mock_load_model):
        """
        Test whether the agent makes a correct action.
        """
        # Create a mock model and set it as the return value for load_model.
        mock_model = Mock()
        mock_load_model.return_value = mock_model

        # Create a PokerAgent object, which will use the mocked `load_model`.
        agent = PokerAgent()

        # Create game state objects.
        gamestate = ClientGameState("coordinator_1", "player_1", 100)
        gameroundstate = ClientGameRoundState("coordinator_1", 1)
        gameroundstate.set_card('K')

        # Mock the available actions for the round.
        gameroundstate.get_available_actions = Mock(return_value=['BET', 'CHECK'])

        # Simulate a situation where the agent should choose the 'BET' action.
        gameroundstate.set_moves_history(['FOLD', 'BET'])
    
        # Call the agent's make_action method again after the history change.
        action = agent.make_action(gamestate, gameroundstate)
        assert action in ['BET', 'CHECK']

    def test_make_action_2(self, agent, client_game_state, game_round):
        """Test various actions based on the player's role and card."""
        # Scenario 1: Initial player, first turn with a card 'J'
        game_round.set_turn_order(1)
        game_round.set_moves_history([])  # No moves made yet
        game_round.set_card('J')  # Initial player has card 'J'

        action = agent.make_action(client_game_state, game_round)
        assert action in ["CHECK", "BET"], f"Expected CHECK or BET, got {action}"
 
        # Scenario 2: Initial player, first turn with a card 'K'
        game_round.set_card('K')
        action = agent.make_action(client_game_state, game_round)
        assert action in ["CHECK", "BET"], f"Expected CHECK or BET, got {action}"

        # Scenario 3: Initial player, responding after a move with card 'K'
        game_round.set_moves_history(["BET"])  # An initial bet has been made
        action = agent.make_action(client_game_state, game_round)
        assert action in ["CALL", "FOLD"], f"Expected CALL or FOLD, got {action}"

    def test_make_action_3(self, agent, client_game_state, game_round):
        # Scenario 4: Responding player, initial move with a card 'J'
        game_round.set_turn_order(2)  # Switch to responding player
        game_round.set_available_actions(["CHECK", "BET"]) 
        game_round.set_card('J')  # Responding player has card 'J'
    
        action = agent.make_action(client_game_state, game_round)
        assert action in ["CHECK", "BET"], f"Expected CHECK or BET, got {action}"

    
    def test_on_image(self, image, agent, game_round):
        """
        Test whether the agent correctly identifies the rank of a card.
        """
        agent.on_image(image, game_round)
        assert game_round.get_card() == "J"

    def test_on_game_start(self, agent):
        """
        Test whether the agent correctly handles the game start
        """
        try:
            agent.on_game_start()  # Call should not raise any exceptions
        except Exception as e:
            pytest.fail(f"on_game_start raised an exception: {e}")