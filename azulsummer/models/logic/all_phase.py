from azulsummer.models.actions import AdvancePhase
from azulsummer.models.actions import AdvanceRound
from azulsummer.models.actions import AdvanceWildTileIndex
from azulsummer.models.actions import AssignCurrentPlayerToStartPlayer
from azulsummer.models.actions import ResetPhaseTurn
from azulsummer.models.actions import ResetStartPlayerToken
from azulsummer.models.enums import Phase
from azulsummer.models.enums import WildTiles
from azulsummer.models.events import CurrentPlayerSet
from azulsummer.models.events import PhaseAdvanced
from azulsummer.models.events import PhaseTurnSetToZero
from azulsummer.models.events import RoundAdvanced
from azulsummer.models.events import StartPlayerTokenWasReset
from azulsummer.models.events import WildTileIndexAdvanced
from azulsummer.models.game import Game


def increment_turn():
    pass


def increment_phase_turn():
    pass


# def generate_draw(action: GenerateTileDraw) -> TileArray:
#     tiles = generate_bag_draw(action.game.state.tiles)
#     action.game.event_queue.append(TileDrawGenerated(action.game, str(tiles)))
#     return tiles


def advance_phase(action: AdvancePhase) -> None:
    """Advance the game's phase"""
    current_phase = action.game.phase
    if current_phase is None:
        action.game.phase = Phase.acquire_tile
    else:
        action.game.phase = Phase((current_phase + 1) % len(Phase))
    action.game.enqueue_event(PhaseAdvanced(action.game, str(action.game.phase)))


def assign_current_player_to_start_player(
    action: AssignCurrentPlayerToStartPlayer,
) -> None:
    """Assign the current_player to the start_token player"""
    if action.game.start_player_index is None:
        player_to_start = 0
    else:
        player_to_start = action.game.start_player_index
    assign_current_player(action.game, player_to_start)


def assign_current_player(game: Game, player_index: int) -> None:
    game.current_player_index = player_index
    game.enqueue_event(CurrentPlayerSet(game=game, player_index=player_index))


def reset_start_player_index_value(action: ResetStartPlayerToken) -> None:
    action.game.start_player_index = None
    action.game.enqueue_event(StartPlayerTokenWasReset(game=action.game))


def advance_round(action: AdvanceRound) -> None:
    """Advance the game's round"""
    current_round = action.game.state.game_round
    if current_round is None:
        action.game.state.game_round = 1
    else:
        action.game.state.game_round += 1
    action.game.event_queue.append(
        RoundAdvanced(game=action.game, round=action.game.state.game_round)
    )


def advance_wild_tile_index(action: AdvanceWildTileIndex) -> None:
    """Advance the Wild Tile index"""
    current_wild_tile = action.game.state.wild_tile
    if current_wild_tile is None:
        action.game.state.wild_tile = WildTiles(0)
    else:
        action.game.state.wild_tile = WildTiles(current_wild_tile + 1)
    action.game.event_queue.append(
        WildTileIndexAdvanced(action.game, str(action.game.state.wild_tile))
    )


def reset_phase_turn(action: ResetPhaseTurn):
    """Reset the Phase Turn to 0 at the start of a phase"""
    action.game.state.phase_turn = 0
    action.game.event_queue.append(PhaseTurnSetToZero(action.game))


def acquire_tile(action):
    # transfer tile to player hand
    # emit event
    # if tile is the middle and flag is None:  reduce player score by n_tiles
    # emit event
    # transfer remainder to middle
    # emit event
    # resolve_phase_one_action()
    pass


def resolve_phase_one_action():
    # evaluate remaining tiles in the factory and middle
    # - If tiles -
    # -- prepare_phase_one_turn()
    # - If not tiles -
    # -- enqueue begin phase 2 action

    pass


def begin_phase_two(action):
    # Advance the phase
    # Advance turn
    # Set phase turn to 0
    # prepare_phase_two_turn()
    pass


def prepare_phase_two_turn(action):
    # Generate available tile plays + pass for the first player and emit those
    # plays
    pass


def play_tile(action):
    # Play tile to board
    # Move tiles from hand to board
    # Update score
    # Evaluate bonus tile draw

    pass


def pass_playing_tiles(action):
    # Generate tiles to keep options and emit back to player
    # Discard remaining tiles
    # Update score
    # Remove player from remaining phase two players
    # Resolve phase two action()
    pass


def resolve_phase_two_action(action):
    # Check if there are still players in phase two
    # - If yes:
    # -- Refill the empty space on the supply spaces
    # -- Advance turn, phase_turn, etc.
    # -- prepare_phase_two_turn()
    # - If no:
    # -- Is it the end of the game?
    # -- If yes: enqueue resolve_end_of_game()
    # -- If no:  begin_phase_three()

    pass


def begin_phase_three(action):
    # Advance the WildTile counter by 1
    # Refill factory displays
    #
    pass


def resolve_end_of_game(action):
    # for each player:
    #   Assess points per store
    #   Assess all 1's, 2's, 3's and 4's
    #   Discard remaining tiles and lose points
    pass
