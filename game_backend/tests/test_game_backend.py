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
    FleetComponent,
)
from game_backend.systems.position_system import PositionSystem
from game_backend.systems.mission_system import MissionSystem

from game_backend.game_structs import PlanetLocation
from game_backend.config import SPEED


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

    metal_mine = earth.buildings["metal_mine"]
    assert metal_mine.components[BuildingComponent].level == 0


def test_serialise_gamestate():
    game_state = initialise_gamestate()

    game_state_dict = game_state.serialise()

    game_state_string = json.dumps(game_state_dict)

    # Deserialisation does not work right now...


#    new_game_state = GameState.from_json(game_state_json)

# assert new_game_state == game_state


def test_ids():
    game_state = initialise_gamestate()

    metal_mine = game_state.world.planets[PlanetLocation(1, 1, 3)].buildings[
        "metal_mine"
    ]

    assert metal_mine.components[ProducerComponent]._entity_id == metal_mine.id
    assert metal_mine.id in EntityCatalog.entities_index


def test_game_update():
    game_state = initialise_gamestate()
    game = Game(game_state)
    earth = game.game_state.world.planets[PlanetLocation(1, 1, 3)]

    game.update(3600)

    assert earth.components[PlanetComponent].resources[Resources.Metal] == 30 * SPEED

    earth.buildings["metal_mine"].components[BuildingComponent].level += 1
    earth.buildings["solar_plant"].components[BuildingComponent].level += 1

    # assert earth.components[PlanetComponent].production_per_second == 800

    game.update(3600)

    assert earth.components[PlanetComponent].resources[Resources.Metal] > 60 * SPEED


def test_upgrade_building():
    game_state = initialise_gamestate()
    game = Game(game_state)

    upgrade_success = game.action_upgrade_building(
        "max", PlanetLocation(1, 1, 3), "metal_mine"
    )

    assert not upgrade_success

    game.update(3600)

    upgrade_success = game.action_upgrade_building(
        "max", PlanetLocation(1, 1, 3), "metal_mine"
    )

    planet_component = game_state.world.planets[PlanetLocation(1, 1, 3)].components[
        PlanetComponent
    ]

    assert upgrade_success
    assert planet_component.resources[Resources.Metal] < 30 * SPEED
    assert int(planet_component.resources[Resources.Cristal]) < 20 * SPEED

    with pytest.raises(AssertionError) as excinfo:
        game.action_upgrade_building("max", "ploup", "metal_mine")

        assert "unkwnown planet" in str(excinfo.value).lower()

    with pytest.raises(AssertionError) as excinfo:
        game.action_upgrade_building("ploup", PlanetLocation(1, 1, 3), "metal_mine")

        assert "unknown player" in str(excinfo.value).lower()


def test_upgrade_research():
    game_state = initialise_gamestate()
    game = Game(game_state)

    game.update(24 * 3600)
    earth = PlanetLocation(1, 1, 3)

    upgrade_success = game.action_upgrade_research("max", earth, "energy")
    assert not upgrade_success

    upgrade_success = game.action_upgrade_building("max", earth, "research_lab")
    assert upgrade_success

    upgrade_success = game.action_upgrade_research("max", earth, "laser")
    assert not upgrade_success

    upgrade_success = game.action_upgrade_research("max", earth, "energy")
    assert upgrade_success

    upgrade_success = game.action_upgrade_research("max", earth, "laser")
    assert not upgrade_success

    upgrade_success = game.action_upgrade_building("max", earth, "research_lab")
    upgrade_sucess = game.action_upgrade_research("max", earth, "energy")

    upgrade_sucess = game.action_upgrade_research("max", earth, "laser")
    assert upgrade_success


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

    game.update(24 * 3600)

    success = game.action_upgrade_building("max", PlanetLocation(1, 1, 3), "shipyard")

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
    fleet_comp = fleet.components[FleetComponent]
    MissionSystem.order_mission(
        fleet,
        "TRANSPORT",
        PlanetLocation(1, 1, 4),
        {Resources.Metal: 2, Resources.Cristal: 0.5},
    )

    game.update(10)

    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 4)
    assert fleet_comp.cargo[Resources.Metal] == 2

    game.update(100),

    assert fleet_comp.mission == "RETURN"
    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 3)
    assert fleet_comp.cargo[Resources.Metal] == 0


def test_fleet_transport_from_game():
    game_state = init_state_complex()

    game = Game(game_state)

    game.update(3600)

    earth = PlanetLocation(1, 1, 3)
    assert (
        game_state.world.planets[earth]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 30 * SPEED
    )

    game.action_send_mission(
        "max",
        PlanetLocation(1, 1, 3),
        "TRANSPORT",
        PlanetLocation(1, 1, 4),
        {Resources.Metal: 2, Resources.Cristal: 2},
    )

    assert (
        game_state.world.planets[earth]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        == 30 * SPEED - 2
    )
    game.update(5)

    fleets = game.get_player_fleets("max")

    fleet_comp = fleets[0].components[FleetComponent]

    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 4)
    assert fleet_comp.cargo[Resources.Metal] == 2

    game.update(100)

    assert fleet_comp.mission == "RETURN"
    assert fleet_comp.travelling_to == PlanetLocation(1, 1, 3)
    assert fleet_comp.cargo[Resources.Metal] == 0


def test_colonize_planet():
    game_state = init_state_complex()
    game = Game(game_state)

    earth = PlanetLocation(1, 1, 3)

    game.update(100)
    game.action_upgrade_building("max", earth, "shipyard")
    game.update(100)
    game.action_build_ship("max", earth, "colony_ship")

    game.action_send_mission(
        "max", earth, "COLONIZE", PlanetLocation(1, 1, 6), cargo={Resources.Metal: 5}
    )

    game.update(25)
    game.update(25)

    assert len(game_state.world.planets) == 4
    new_planet = game_state.world.planets[PlanetLocation(1, 1, 6)]
    new_planet_comp = new_planet.components[PlanetComponent]

    assert new_planet.buildings["metal_mine"].components[BuildingComponent].level == 0


def test_combat():
    game_state = init_state_complex()
    game = Game(game_state)

    earth = PlanetLocation(1, 1, 3)
    jupiter = PlanetLocation(1, 1, 5)

    game_state.world.planets[jupiter].buildings["metal_mine"].components[
        BuildingComponent
    ].level = 0

    game.update(360)

    game.action_send_mission("max", earth, "ATTACK", jupiter)

    attacking_fleet = game_state.players["max"].fleets[0]

    assert attacking_fleet.components[FleetComponent].mission == "ATTACK"
    assert attacking_fleet.ships[0].components[ShipComponent].number == 10
    assert attacking_fleet.components[FleetComponent].cargo == {
        Resources.Metal: 0,
        Resources.Cristal: 0,
        Resources.Deuterium: 0,
    }

    travelling_time = attacking_fleet.components[FleetComponent].travel_time_left

    game.update(travelling_time - 1)

    assert (
        game_state.world.planets[jupiter]
        .components[PlanetComponent]
        .resources[Resources.Metal]
        > 0
    )

    game.update(1)

    assert game_state.world.planets[jupiter].components[PlanetComponent].resources == {
        Resources.Metal: 0,
        Resources.Cristal: 0,
        Resources.Deuterium: 0,
    }
    assert len(game_state.players["bob"].fleets) == 0
    assert attacking_fleet.ships[0].components[ShipComponent].number == 7
    assert attacking_fleet.components[FleetComponent].cargo[Resources.Metal] > 0
    assert attacking_fleet.components[FleetComponent].cargo[Resources.Cristal] > 0
    assert attacking_fleet.components[FleetComponent].cargo[Resources.Deuterium] > 0
    game.update(20)
