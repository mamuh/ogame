from game_backend import __version__
from game_backend.init_game import initialise_gamestate
from game_backend.game import Game
from game_backend.resources import Resources
from game_backend.entities import GameState
from game_backend.ecs.entity import EntityCatalog
from game_backend.components import (
    PlayerComponent,
    ProducerComponent,
    PlanetComponent,
    BuildingComponent,
)
import game_backend.entities


def test_version():
    assert __version__ == "0.1.0"


def test_initialise_gamestate():
    game_state = initialise_gamestate()

    assert len(game_state.players) == 1
    assert "max" in game_state.players
    assert game_state.players["max"].components[PlayerComponent].name == "Max"

    assert "earth" in game_state.world.planets
    earth = game_state.world.planets["earth"]

    assert earth.components[PlanetComponent].name == "Earth"

    mine = earth.buildings[0]
    assert mine.components[BuildingComponent].name == "Mine"


def test_serialise_gamestate():
    game_state = initialise_gamestate()

    game_state_dict = game_state.serialise()

    # Deserialisation does not work right now...


#    new_game_state = GameState.from_json(game_state_json)

# assert new_game_state == game_state


def test_ids():
    game_state = initialise_gamestate()

    mine = game_state.world.planets["earth"].buildings[0]

    assert mine.components[ProducerComponent]._entity_id == mine.id
    assert mine.id in EntityCatalog.entities_index


def test_game_update():
    game_state = initialise_gamestate()
    game = Game(game_state)

    game.update(10)

    assert (
        game.game_state.world.planets["earth"]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 10
    )

    game_state.world.planets["earth"].buildings[0].components[
        BuildingComponent
    ].level += 1

    game.update(10)

    assert (
        game.game_state.world.planets["earth"]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 21
    )
