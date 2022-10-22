"""Module containing the game logic """
from azulsummer.models.actions import AdvancePhase
from azulsummer.models.actions import AdvanceRound
from azulsummer.models.actions import AdvanceWildTileIndex
from azulsummer.models.actions import InitializeGameState
from azulsummer.models.actions import PreparePhaseOne
from azulsummer.models.actions import ResetPhaseTurn
from azulsummer.models.actions import StartGame
from azulsummer.models.events import BagLoadedWith132Tiles
from azulsummer.models.events import GameCreatedWithNFactoryDisplays
from azulsummer.models.events import GameCreatedWithNPlayers
from azulsummer.models.events import GameStarted
from azulsummer.models.events import GameStateInitialized
from azulsummer.models.events import PlayerScoresInitializedAt5


def start_game(action: StartGame):
    action.game.enqueue_action(InitializeGameState(game=action.game))
    action.game.enqueue_event(GameStarted(game=action.game))


def initialize_game_state(action: InitializeGameState):
    action.game.make_state()  # Creates the new game state

    events = [
        GameStateInitialized(game=action.game),
        GameCreatedWithNPlayers(
            game=action.game, n_players=len(action.game.players)
        ),
        BagLoadedWith132Tiles(game=action.game),
        GameCreatedWithNFactoryDisplays(
            game=action.game,
            n_factory_displays=action.game.n_factory_displays,
        ),
        PlayerScoresInitializedAt5(game=action.game),
    ]
    actions = [
        AdvancePhase(game=action.game),
        AdvanceRound(game=action.game),
        AdvanceWildTileIndex(game=action.game),
        ResetPhaseTurn(game=action.game),
        PreparePhaseOne(game=action.game),
    ]

    for event in events:
        action.game.enqueue_event(event)

    for action_ in actions:
        action.game.enqueue_action(action_)
