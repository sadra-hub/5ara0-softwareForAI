import random
from model import load_model, identify
from client.state import ClientGameRoundState, ClientGameState
from strategy import initial_player, responding_player


class PokerAgent(object):

    def __init__(self):
        self.model = load_model()

    def make_action(self, state: ClientGameState, round: ClientGameRoundState) -> str:
        """
        Next action, used to choose a new action depending on the current state of the game. This method implements your
        PokerBot strategy. Use the state and round arguments to decide the next best move.

        Parameters
        ----------
        state : ClientGameState
            State object of the current game (a game has multiple rounds)
        round : ClientGameRoundState
            State object of the current round (from deal to showdown)

        Returns
        -------
        str in ['BET', 'CALL', 'CHECK', 'FOLD'] (and in round.get_available_actions())
            A string representation of the next action an agent wants to do next, should be from a list of available actions
        """

        if round.get_turn_order() == 1:
            return initial_player(round)
        else:
            return responding_player(round)

    def on_image(self, image, round: ClientGameRoundState):
        """
        This method is called every time when the card image changes. Use this method for image recongition.

        Parameters
        ----------
        image : Image
            Image object
        """

        rank = identify(image, self.model)
        return round.set_card(rank)

    def on_error(self, error):
        """
        This methods will be called in case of error either from the server backend or from the client itself.
        You can also use this function for error handling.

        Parameters
        ----------
        error : str
            string representation of the error
        """
        print(error)

    def on_game_start(self):
        """
        This method will be called once at the beginning of the game when the server has confirmed that both players are connected.
        """
        print('Game has started.')

    def on_new_round_request(self, state: ClientGameState):
        """
        This method is called every time before a new round is started. A new round is started automatically.
        You can use this method for logging purposes.

        Parameters
        ----------
        state : ClientGameState
            State object of the current game
        """
        print("New round has been started. Currently in the bank: ", state.get_player_bank())

    def on_round_end(self, state: ClientGameState, round: ClientGameRoundState):
        """
        This method is called every time a round has ended. A round ends automatically. 
        You can use this method for logging purposes.

        Parameters
        ----------
        state : ClientGameState
            State object of the current game
        round : ClientGameRoundState
            State object of the current round
        """
        print(f'----- Round { round.get_round_id() } results ----- ')
        print(f'  Your card       : { round.get_card() }')
        print(f'  Your turn order : { round.get_turn_order() }')
        print(f'  Moves history   : { round.get_moves_history() }')
        print(f'  Your outcome    : { round.get_outcome() }')
        print(f'  Current bank    : { state.get_player_bank() }')
        print(f'  Show-down       : { round.get_cards() }')

    def on_game_end(self, state: ClientGameState, result: str):
        """
        This method is called once after the game has ended. A game ends automatically. 
        You can use this method for logging purposes.

        Parameters
        ----------
        state : ClientGameState
            State object of the current game
        result : str in ['WIN', 'DEFEAT']
            End result of the game
        """
        print(f'----- Game results ----- ')
        print(f'  Outcome:    { result }')
        print(f'  Final bank: { state.get_player_bank() }')
