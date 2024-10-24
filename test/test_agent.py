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
    
    def test_on_image(self, image, agent):
        """
        Test whether the agent correctly identifies the rank of a card.
        """
        rank = agent.on_image(image)
    
        # Assert that the returned rank is 'J' for the image "J_1.png"
        assert rank == 'J'

    def test_on_game_start(self, agent):
        """
        Test whether the agent correctly handles the game start
        """
        try:
            agent.on_game_start()  # Call should not raise any exceptions
        except Exception as e:
            pytest.fail(f"on_game_start raised an exception: {e}")

    def test_on_new_round_request(agent, client_game_state):
    
        """
        test whether the agent correctly handles the new round request
        """
        try:
            agent.on_new_round_request(client_game_state)  # Call should not raise any exceptions
        except Exception as e:
            pytest.fail(f"on_new_round_request raised an exception: {e}")

        # Player bank is positive before start of new round
        assert not client_game_state.get_player_bank() < 0  

    def test_on_game_end(agent, client_game_state):
        """
        test whether the agent correctly handles the end of a game
        """
        try:
            agent.on_game_end(client_game_state, 'WIN')  
        except Exception as e:
            pytest.fail(f"on_game_end raised an exception: {e}")

    def test_on_round_end(agent, client_game_state, game_round):
        # Simulate the end of a round
        try:
            agent.on_round_end(client_game_state, game_round)  
        except Exception as e:
            pytest.fail(f"on_round_end raised an exception: {e}")