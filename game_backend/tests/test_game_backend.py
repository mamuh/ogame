import json
import pytest

from game_backend import __version__
from game_backend.init_game import initialise_gamestate, initialise_empty_universe
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

    mine = earth.buildings["mine"]
    assert mine.components[BuildingComponent].name == "Mine"


def test_serialise_gamestate():
    game_state = initialise_gamestate()

    game_state_dict = game_state.serialise()

    game_state_string = json.dumps(game_state_dict)

    # Deserialisation does not work right now...


#    new_game_state = GameState.from_json(game_state_json)

# assert new_game_state == game_state


def test_ids():
    game_state = initialise_gamestate()

    mine = game_state.world.planets["earth"].buildings["mine"]

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

    game_state.world.planets["earth"].buildings["mine"].components[
        BuildingComponent
    ].level += 1

    game.update(10)

    assert (
        game.game_state.world.planets["earth"]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 21
    )


def test_upgrade_building():
    game_state = initialise_gamestate()
    game = Game(game_state)

    upgrade_success = game.action_upgrade_building("max", "earth", "mine")

    assert not upgrade_success

    game.update(110)

    upgrade_success = game.action_upgrade_building("max", "earth", "mine")

    planet_component = game_state.world.planets["earth"].components[PlanetComponent]

    assert upgrade_success
    assert planet_component.resources[Resources.Metal] == 100
    assert planet_component.resources[Resources.Oil] == 1.1

    with pytest.raises(AssertionError) as excinfo:
        game.action_upgrade_building("max", "ploup", "mine")

        assert "unkwnown planet" in str(excinfo.value).lower()

    with pytest.raises(AssertionError) as excinfo:
        game.action_upgrade_building("ploup", "earth", "mine")

        assert "unknown player" in str(excinfo.value).lower()


def test_empty_universe():
    game_state = initialise_empty_universe(100)

    assert len(game_state.world.planets) == 100


def test_create_new_player():
    game_state = initialise_empty_universe(100)

    game = Game(game_state)

    success = game.create_new_player("john", "John")

    assert success

    assert (
        game_state.world.planets["planet_0"].components[PlanetComponent].owner_id
        == "john"
    )

    success = game.create_new_player("john", "Michel")

    assert not success
