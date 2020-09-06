import json
import pytest

from game_backend import __version__
from game_backend.init_game import (
    initialise_gamestate,
    initialise_empty_universe,
    init_state_complex,
)
from game_backend.game import Game
from game_backend.resources import Resources
from game_backend.entities.entities import GameState
from game_backend.ecs.entity import EntityCatalog
from game_backend.components import (
    PlayerComponent,
    ProducerComponent,
    PlanetComponent,
    BuildingComponent,
    ShipComponent,
    FleetPositionComponent,
)
from game_backend.systems.position_system import PositionSystem
from game_backend.systems.mission_system import MissionSystem

from game_backend.game_structs import PlanetLocation


@pytest.fixture(autouse=True, scope="function")
def teardown(request):
    def fin():
        PositionSystem.reset()

    request.addfinalizer(fin)


def test_version():
    assert __version__ == "0.1.0"


def test_initialise_gamestate():
    game_state = initialise_gamestate()

    assert len(game_state.players) == 1
    assert "max" in game_state.players
    assert game_state.players["max"].components[PlayerComponent].name == "Max"

    assert PlanetLocation(1, 1, 3) in game_state.world.planets
    earth = game_state.world.planets[PlanetLocation(1, 1, 3)]

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

    mine = game_state.world.planets[PlanetLocation(1, 1, 3)].buildings["mine"]

    assert mine.components[ProducerComponent]._entity_id == mine.id
    assert mine.id in EntityCatalog.entities_index


def test_game_update():
    game_state = initialise_gamestate()
    game = Game(game_state)

    game.update(10)

    assert (
        game.game_state.world.planets[PlanetLocation(1, 1, 3)]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 10
    )

    game_state.world.planets[PlanetLocation(1, 1, 3)].buildings["mine"].components[
        BuildingComponent
    ].level += 1

    game.update(10)

    assert (
        game.game_state.world.planets[PlanetLocation(1, 1, 3)]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 21
    )


def test_upgrade_building():
    game_state = initialise_gamestate()
    game = Game(game_state)

    upgrade_success = game.action_upgrade_building(
        "max", PlanetLocation(1, 1, 3), "mine"
    )

    assert not upgrade_success

    game.update(110)

    upgrade_success = game.action_upgrade_building(
        "max", PlanetLocation(1, 1, 3), "mine"
    )

    planet_component = game_state.world.planets[PlanetLocation(1, 1, 3)].components[
        PlanetComponent
    ]

    assert upgrade_success
    assert planet_component.resources[Resources.Metal] == 100
    assert planet_component.resources[Resources.Oil] == 55

    with pytest.raises(AssertionError) as excinfo:
        game.action_upgrade_building("max", "ploup", "mine")

        assert "unkwnown planet" in str(excinfo.value).lower()

    with pytest.raises(AssertionError) as excinfo:
        game.action_upgrade_building("ploup", PlanetLocation(1, 1, 3), "mine")

        assert "unknown player" in str(excinfo.value).lower()


def test_create_new_player():
    game_state = initialise_empty_universe()

    game = Game(game_state)

    success = game.create_new_player("john", "John")

    assert success

    john_planets = PositionSystem.get_player_planets("john")

    assert (
        game_state.world.planets[john_planets[0]].components[PlanetComponent].owner_id
        == "john"
    )

    success = game.create_new_player("john", "Michel")

    assert not success


def test_build_ship():
    game_state = initialise_gamestate()

    game = Game(game_state)

    outcome = game.action_build_ship("max", PlanetLocation(1, 1, 3), "light_fighter")

    assert not outcome.success

    game.update(1000)

    success = game.action_upgrade_building("max", PlanetLocation(1, 1, 3), "ship_yard")

    assert success

    outcome = game.action_build_ship("max", PlanetLocation(1, 1, 3), "light_fighter")

    assert outcome.success

    assert len(game_state.players["max"].fleets) == 1
    assert (
        game_state.players["max"]
        .fleets[0]
        .light_fighter.components[ShipComponent]
        .number
        == 1
    )


def test_fleet_transport():
    game_state = init_state_complex()

    game = Game(game_state)

    game.update(100)
    fleet = game_state.players["max"].fleets[0]
    fleet_comp = fleet.components[FleetPositionComponent]
    MissionSystem.order_mission(
        fleet,
        "TRANSPORT",
        PlanetLocation(1, 1, 4),
        {Resources.Metal: 2, Resources.Oil: 0.5},
    )

    game.update(5)

    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 4)
    assert fleet_comp.cargo[Resources.Metal] == 2

    game.update(10),

    assert fleet_comp.mission == "RETURN"
    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 3)
    assert fleet_comp.cargo[Resources.Metal] == 0


def test_fleet_transport_from_game():
    game_state = init_state_complex()

    game = Game(game_state)

    game.update(100)

    game.action_send_mission(
        "max",
        PlanetLocation(1, 1, 3),
        "TRANSPORT",
        PlanetLocation(1, 1, 4),
        {Resources.Metal: 2, Resources.Oil: 0.5},
    )

    game.update(5)

    fleets = game.get_player_fleets("max")

    fleet_comp = fleets[0].components[FleetPositionComponent]

    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 4)
    assert fleet_comp.cargo[Resources.Metal] == 2

    game.update(10)

    assert fleet_comp.mission == "RETURN"
    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 3)
    assert fleet_comp.cargo[Resources.Metal] == 0


def test_colonize_planet():
    game_state = init_state_complex()
    game = Game(game_state)

    earth = PlanetLocation(1, 1, 3)

    game.update(100)
    game.action_upgrade_building("max", earth, "ship_yard")
    game.update(100)
    game.action_build_ship("max", earth, "colony_ship")

    game.action_send_mission(
        "max", earth, "COLONIZE", PlanetLocation(1, 1, 5), cargo={Resources.Metal: 5}
    )

    game.update(15)
    game.update(15)

    assert len(game_state.world.planets) == 3
    new_planet = game_state.world.planets[PlanetLocation(1, 1, 5)]
    new_planet_comp = new_planet.components[PlanetComponent]

    assert new_planet_comp.resources[Resources.Metal] == 5

    game.update(15)

    assert new_planet_comp.resources[Resources.Metal] == 20
    assert new_planet.buildings["mine"].components[BuildingComponent].level == 0
