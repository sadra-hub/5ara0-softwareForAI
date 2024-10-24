import pytest
from client.state import ClientGameRoundState

class TestClientGameState:

    def test_initial_attributes(self, client_game_state):
        """
        Test the initial attributes of the ClientGameState instance.

        Ensures that the coordinator ID, player token, player bank, and rounds are 
        initialized with the correct values.
        """
        assert client_game_state.get_coordinator_id() == "coordinator_1"
        assert client_game_state.get_player_token() == "player_1"
        assert client_game_state.get_player_bank() == 100
        assert client_game_state.get_rounds() == []
    def test_update_bank(self, client_game_state):
        """
        Test the update_bank() method.

        Verifies that the player's bank is correctly updated by adding and subtracting 
        amounts to the initial bank value.
        """
        client_game_state.update_bank(20)
        assert client_game_state.get_player_bank() == 120

        client_game_state.update_bank(-50)
        assert client_game_state.get_player_bank() == 70

    def test_start_new__empty_round(self, client_game_state):
        """
        Test starting a new round when no moves are made.

        Ensures that starting a new round without any moves does not add a round to 
        the list of rounds and that the last round state is correctly initialized.
        """
        client_game_state.start_new_round()
        # Rounds with no move should be filtered out
        assert len(client_game_state.get_rounds()) == 0
        assert client_game_state.get_last_round_state().get_round_id() == 1

    def test_get_rounds_with_moves(self, client_game_state):
        """
        Test where only rounds with move history are returned.

        Adds one round without moves and one round with a move, then ensures that 
        only the round with a move is returned from the get_rounds() method.
        """
        # Add a round without moves
        round_without_moves = ClientGameRoundState(client_game_state.get_coordinator_id(), 1)
        client_game_state._rounds.append(round_without_moves)

        # Add a round with moves
        round_with_moves = ClientGameRoundState(client_game_state.get_coordinator_id(), 2)
        round_with_moves.add_move_history("BET")
        client_game_state._rounds.append(round_with_moves)

        assert len(client_game_state.get_rounds()) == 1  # Should only return the round with moves
        assert client_game_state.get_rounds()[0].get_round_id() == 2