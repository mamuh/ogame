from game_backend import __version__
from game_backend.init_game import initialise_gamestate
from game_backend.game import Game
from game_backend.game_model import Resources


def test_version():
    assert __version__ == "0.1.0"


def test_initialise_gamestate():
    game_state = initialise_gamestate()

    assert len(game_state.players) == 1
    assert "max" in game_state.players
    assert game_state.players["max"].name == "Max"

    assert "earth" in game_state.world.planets
    earth = game_state.world.planets["earth"]

    assert earth.name == "Earth"


def test_game_update():
    game_state = initialise_gamestate()
    game = Game(game_state)

    game.update(10)

    assert game.game_state.players["max"].resources[Resources.Metal] == 10
