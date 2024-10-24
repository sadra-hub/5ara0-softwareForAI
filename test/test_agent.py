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
