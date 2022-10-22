
from azulsummer.models.game import Game
from azulsummer.models.game_handler import GameHandler
from azulsummer.players.actiononeplayer import ActionOnePlayer


players = [ActionOnePlayer() for _ in range(4)]
game = Game.new(players)
gh = GameHandler(game)
gh.play()
