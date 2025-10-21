from client.state import ClientGameRoundState, ClientGameState
import random

def initial_player(round: ClientGameRoundState):
    """
    Strategy for the initial player, depending on whether the game just started or if a betting action has been made.
    
    If no actions have been made (game just started), the player will decide whether to CHECK or BET based on the card they hold.
    If an action has been made, the player will decide whether to CALL or FOLD based on the card and the move history.
    
    :param round: The current game round state, containing information about the player's card and move history.
    :return: The selected action, either "CHECK", "BET", "CALL", or "FOLD".
    """
    
    alpha = random.uniform(0, 1/3)
    
    # Probabilities for the initial player when deciding to CHECK or BET
    initial_probs_check_bet = {'J': [1 - alpha, alpha], 'K': [1 - (3 * alpha), 3 * alpha], 'Q': [1, 0]}
    # Probabilities for the initial player when deciding to CALL or FOLD
    initial_probs_call_fold = {'J': [0, 1], 'K': [1, 0], 'Q': [1/3 + alpha, 2/3 - alpha]}

    card = round.get_card()
    move_history = round.get_moves_history()

    if not move_history:  # No moves, meaning it's the first action of the round
        weights = initial_probs_check_bet[card]
        action = random.choices(["CHECK", "BET"], weights=weights)[0]
        return action
    else:  # Moves have been made, respond to the bet with CALL or FOLD
        weights = initial_probs_call_fold[card]
        action = random.choices(["CALL", "FOLD"], weights=weights)[0]
        return action

def responding_player(round: ClientGameRoundState):
    """
    Strategy for the responding player, depending on whether the initial player checked or bet.
    
    If the initial player checks, the responding player will decide whether to check or bet based on their card.
    If the initial player bets, the responding player will decide whether to call or fold.
    
    :param round: The current game round state, containing information about the player's card and available actions.
    :return: The selected action, either "CHECK", "BET", "CALL", or "FOLD".
    """
    
    card = round.get_card()
    available_actions = round.get_available_actions()

    # Probabilities for the responding player when deciding to CHECK or BET
    responding_probs_check_bet = {'J': [2/3, 1/3], 'K': [0, 1], 'Q': [1, 0]}
    # Probabilities for the responding player when deciding to CALL or FOLD
    responding_probs_call_fold = {'J': [0, 1], 'K': [1, 0], 'Q': [1/3, 2/3]}
    
    if "BET" in available_actions: # If the initial player checked, the responding player can bet or check
        weights = responding_probs_check_bet[card]
        action = random.choices(["CHECK", "BET"], weights=weights)[0]
        return action
    else:  # If the initial player bet, the responding player chooses between calling or folding
        weights = responding_probs_call_fold[card]
        action = random.choices(["CALL", "FOLD"], weights=weights)[0]
        return action