from typing import List, Dict

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities.entities import GameState
from game_backend.components import (
    FleetPositionComponent,
    ShipComponent,
    PlanetPositionComponent,
    PlanetComponent,
)
from game_backend.entities.ships import Fleet
from game_backend.resources import (
    Resources,
    add_resources,
    empty_resources,
    sufficient_funds,
    subtract_cost,
)


VALID_MISSIONS = ["TRANSPORT", "RETURN"]


class MissionSystem:
    def update(self, dt):
        game_state: GameState = EntityCatalog.get_special("game_state")

        for player in game_state.players.values():
            for fleet in player.fleets:
                fleet_pos_comp = fleet.components[FleetPositionComponent]
                if not fleet_pos_comp.in_transit:
                    continue

                fleet_pos_comp.travel_time_left -= dt

                if fleet_pos_comp.travel_time_left <= 0:
                    self.execute_mission(game_state, fleet)

    def execute_mission(self, game_state: GameState, fleet: Fleet):
        fleet_pos_comp = fleet.components[FleetPositionComponent]
        if fleet_pos_comp.mission == "TRANSPORT":
            destination_planet = game_state.world.planets[fleet_pos_comp.travelling_to]
            dest_planet_comp = destination_planet.components[PlanetComponent]
            dest_planet_comp.resources = add_resources(
                dest_planet_comp.resources, fleet_pos_comp.cargo
            )
            fleet_pos_comp.cargo = empty_resources()

            fleet_pos_comp.mission = "RETURN"
            prev_destination = fleet_pos_comp.travelling_to
            fleet_pos_comp.travelling_to = fleet_pos_comp.travelling_from
            fleet_pos_comp.travelling_from = prev_destination

            fleet_pos_comp.travel_time_total = self.compute_travelling_time(
                game_state,
                fleet,
                fleet_pos_comp.travelling_from,
                fleet_pos_comp.travelling_to,
            )

            fleet_pos_comp.travel_time_left = fleet_pos_comp.travel_time_total

        elif fleet_pos_comp.mission == "RETURN":
            destination_planet = game_state.world.planets[fleet_pos_comp.travelling_to]
            destination_planet.resources = add_resources(
                destination_planet.resources, fleet_pos_comp.cargo
            )
            fleet_pos_comp.cargo = empty_resources()

            fleet_pos_comp.current_planet_id = fleet_pos_comp.travelling_to
            fleet_pos_comp.in_transit = False
            fleet_pos_comp.travelling_to = (
                fleet_pos_comp.travelling_from
            ) = (
                fleet_pos_comp.mission
            ) = fleet_pos_comp.travel_time_total = fleet_pos_comp.travel_time_left = 0

    def compute_travelling_time(
        self, game_state: GameState, fleet: Fleet, from_id: str, to_id: str
    ):
        planet_from = game_state.world.planets[from_id]
        planet_to = game_state.world.planets[to_id]

        ships = fleet.get_ships()

        fleet_speed = min([ship.components[ShipComponent].speed for ship in ships])

        galaxy_from = planet_from.components[PlanetPositionComponent].galaxy
        system_from = planet_from.components[PlanetPositionComponent].solar_system
        position_from = planet_from.components[PlanetPositionComponent].position

        galaxy_to = planet_to.components[PlanetPositionComponent].galaxy
        system_to = planet_to.components[PlanetPositionComponent].solar_system
        position_to = planet_to.components[PlanetPositionComponent].position

        total_distance = (
            abs(galaxy_to - galaxy_from) * 1000
            + abs(system_to - system_from) * 100
            + abs(position_to - position_from) * 10
        )

        travelling_time = total_distance / fleet_speed

        return travelling_time

    def order_mission(
        self,
        fleet: Fleet,
        mission: str,
        destination_id: str,
        cargo: Dict[Resources, float] = None,
    ):
        game_state: GameState = EntityCatalog.get_special("game_state")
        if cargo is None:
            cargo = emtpy_resources()

        fleet_comp = fleet.components[FleetPositionComponent]

        assert (
            not fleet_comp.in_transit
        ), "Cannot assign mission to fleet already in transit"
        assert mission in VALID_MISSIONS, f"Invalid mission: {mission}"
        assert (
            destination_id in game_state.world.planets
        ), f"Cannot find planet_id {destination_id}"

        planet_from = game_state.world.planets[fleet_comp.current_planet_id]
        planet_comp = planet_from.components[PlanetComponent]
        assert sufficient_funds(
            cargo, planet_comp.resources
        ), "Insufficient resources on planet"

        planet_from.resources = subtract_cost(cargo, planet_comp.resources)
        fleet_comp.mission = mission
        fleet_comp.cargo = cargo
        fleet_comp.in_transit = True
        fleet_comp.travelling_from = fleet_comp.current_planet_id
        fleet_comp.travelling_to = destination_id
        fleet_comp.travel_time_total = self.compute_travelling_time(
            game_state, fleet, fleet_comp.travelling_from, destination_id
        )
        fleet_comp.travel_time_left = fleet_comp.travel_time_total
        fleet_comp.current_planet_id = None


MissionSystem = MissionSystem()
