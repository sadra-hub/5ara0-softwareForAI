import pytest
from client.state import ClientGameRoundState

class TestClientGameState:

    def test_initial_attributes(self, client_game_state):
        assert client_game_state.get_coordinator_id() == "coordinator_1"
        assert client_game_state.get_player_token() == "player_1"
        assert client_game_state.get_player_bank() == 100
        assert client_game_state.get_rounds() == []
    def test_update_bank(self, client_game_state):
        client_game_state.update_bank(20)
        assert client_game_state.get_player_bank() == 120

        client_game_state.update_bank(-50)
        assert client_game_state.get_player_bank() == 70

    def test_start_new__empty_round(self, client_game_state):
        client_game_state.start_new_round()
        # Rounds with no move should be filtered out
        assert len(client_game_state.get_rounds()) == 0
        assert client_game_state.get_last_round_state().get_round_id() == 1

    def test_get_rounds_with_moves(self, client_game_state):
        # Add a round without moves
        round_without_moves = ClientGameRoundState(client_game_state.get_coordinator_id(), 1)
        client_game_state._rounds.append(round_without_moves)

        # Add a round with moves
        round_with_moves = ClientGameRoundState(client_game_state.get_coordinator_id(), 2)
        round_with_moves.add_move_history("BET")
        client_game_state._rounds.append(round_with_moves)

        assert len(client_game_state.get_rounds()) == 1  # Should only return the round with moves
        assert client_game_state.get_rounds()[0].get_round_id() == 2