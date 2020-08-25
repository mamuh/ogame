from game_backend import __version__
from game_backend.init_game import initialise_gamestate


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
