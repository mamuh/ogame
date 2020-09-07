from typing import List, Dict

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities.entities import GameState, Planet
from game_backend.components import (
    FleetPositionComponent,
    ShipComponent,
    PlanetComponent,
)
from game_backend.entities.ships import Fleet
from game_backend.systems.position_system import PositionSystem
from game_backend.resources import (
    Resources,
    add_resources,
    empty_resources,
    sufficient_funds,
    subtract_cost,
)
from game_backend.game_structs import PlanetLocation


VALID_MISSIONS = ["TRANSPORT", "RETURN", "COLONIZE"]


class MissionException(Exception):
    pass


class MissionSystem:
    def update(self, dt):
        # TODO Make sure there is only one fleet per planet at the end of this update
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
            dest_planet_comp = destination_planet.components[PlanetComponent]
            dest_planet_comp.resources = add_resources(
                dest_planet_comp.resources, fleet_pos_comp.cargo
            )
            fleet_pos_comp.cargo = empty_resources()

            fleet_pos_comp.current_location = fleet_pos_comp.travelling_to
            fleet_pos_comp.in_transit = False
            fleet_pos_comp.travelling_to = (
                fleet_pos_comp.travelling_from
            ) = (
                fleet_pos_comp.mission
            ) = fleet_pos_comp.travel_time_total = fleet_pos_comp.travel_time_left = 0

        elif fleet_pos_comp.mission == "COLONIZE":
            if not PositionSystem.is_location_free(fleet_pos_comp.travelling_to):
                self.finish_mission_and_return(fleet)
            else:
                # Remove one colony ship
                fleet.colony_ship.components[ShipComponent].number -= 1
                # Create new planet
                planet_id = fleet_pos_comp.travelling_to
                # TODO: generate size
                planet = Planet.new(
                    name=str(planet_id),
                    planet_id=planet_id,
                    size=250,
                    location=planet_id,
                    owner_id=fleet.owner_id,
                )
                game_state.world.planets[planet_id] = planet

                # Deposit cargo
                planet_comp = planet.components[PlanetComponent]
                planet_comp.resources = add_resources(
                    planet_comp.resources, fleet_pos_comp.cargo
                )
                fleet_pos_comp.cargo = empty_resources()

                # Fleet stays at new planet
                self.stop_fleet(fleet)

    def finish_mission_and_return(self, fleet: Fleet):
        fleet_comp = fleet.components[FleetPositionComponent]
        assert fleet_comp.in_transit
        fleet_comp.mission = "RETURN"
        prev_destination = fleet_comp.travelling_to
        fleet_comp.travelling_to = fleet_comp.travelling_from
        fleet_comp.travelling_from = prev_destination
        fleet_comp.travel_time_left = fleet_comp.travel_time_total

    def stop_fleet(self, fleet: Fleet):
        """
        Stops a fleet when it has reached its destination. It wont be in transit anymore
        """
        fleet_comp = fleet.components[FleetPositionComponent]
        fleet_comp.current_location = fleet_comp.travelling_to
        fleet_comp.in_transit = False
        fleet_comp.travelling_to = (
            fleet_comp.travelling_from
        ) = fleet_comp.mission = None
        fleet_comp.travel_time_total = fleet_comp.travel_time_left = 0

    def compute_travelling_time(
        self,
        game_state: GameState,
        fleet: Fleet,
        from_id: PlanetLocation,
        to_id: PlanetLocation,
    ):
        fleet_comp = fleet.components[FleetPositionComponent]
        ships = fleet.get_ships()

        fleet_speed = min([ship.components[ShipComponent].speed for ship in ships])

        total_distance = fleet_comp.travelling_from.distance_from(
            fleet_comp.travelling_to
        )
        travelling_time = total_distance / fleet_speed

        return travelling_time

    def get_planet_fleet(self, player_id: str, planet_id: PlanetLocation) -> Fleet:
        """
        Returns None if no fleet was found at this planet
        """
        game_state: GameState = EntityCatalog.get_special("game_state")

        assert player_id in game_state.players
        player = game_state.players[player_id]

        for fleet in player.fleets:
            fleet_comp = fleet.components[FleetPositionComponent]
            if not fleet_comp.in_transit and fleet_comp.current_location == planet_id:
                # There should only be one per planet so we can return it...
                return fleet
        # if nothing was found, will return None

    def order_mission(
        self,
        fleet: Fleet,
        mission: str,
        destination_id: str,
        cargo: Dict[Resources, float] = None,
    ):
        game_state: GameState = EntityCatalog.get_special("game_state")
        if cargo is None:
            cargo = empty_resources()

        fleet_comp = fleet.components[FleetPositionComponent]

        assert (
            not fleet_comp.in_transit
        ), "Cannot assign mission to fleet already in transit"
        assert mission in VALID_MISSIONS, f"Invalid mission: {mission}"

        if mission != "COLONIZE":
            assert (
                destination_id in game_state.world.planets
            ), f"Cannot find planet id {destination_id}"

        planet_from = game_state.world.planets[fleet_comp.current_location]
        planet_comp = planet_from.components[PlanetComponent]
        if not sufficient_funds(cargo, planet_comp.resources):
            raise MissionException("Insufficient resources on planet")

        planet_from.resources = subtract_cost(cargo, planet_comp.resources)
        fleet_comp.mission = mission
        fleet_comp.cargo = cargo
        fleet_comp.in_transit = True
        fleet_comp.travelling_from = fleet_comp.current_location
        fleet_comp.travelling_to = destination_id
        fleet_comp.travel_time_total = self.compute_travelling_time(
            game_state, fleet, fleet_comp.travelling_from, destination_id
        )
        fleet_comp.travel_time_left = fleet_comp.travel_time_total
        fleet_comp.current_location = None


MissionSystem = MissionSystem()