from typing import List, Dict
import math

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities.entities import GameState, Planet
from game_backend.components import (
    FleetComponent,
    ShipComponent,
    PlanetComponent,
)
from game_backend.entities.ships import Fleet
from game_backend.systems.position_system import PositionSystem
from game_backend.systems.combat_system import CombatSystem
from game_backend.resources import (
    Resources,
    add_resources,
    empty_resources,
    sufficient_funds,
    subtract_cost,
    RESOURCES_PRIORITY,
)
from game_backend.game_structs import PlanetLocation
from game_backend.config import SPEED


VALID_MISSIONS = ["TRANSPORT", "RETURN", "COLONIZE", "ATTACK"]


class MissionException(Exception):
    pass


class MissionSystem:
    def update(self, dt):
        # TODO Make sure there is only one fleet per planet at the end of this update
        game_state: GameState = EntityCatalog.get_special("game_state")

        for player in game_state.players.values():
            for fleet in player.fleets:
                fleet_comp = fleet.components[FleetComponent]
                if not fleet_comp.in_transit:
                    continue

                fleet_comp.travel_time_left -= dt

                if fleet_comp.travel_time_left <= 0:
                    self.execute_mission(game_state, fleet)

            # Merge fleets on the same planet
            planets_to_fleet = {}
            for fleet in player.fleets:
                fleet_comp = fleet.components[FleetComponent]
                if fleet_comp.in_transit:
                    continue
                planets_to_fleet.setdefault(fleet_comp.current_location, []).append(
                    fleet
                )
            for fleets in planets_to_fleet.values():
                if len(fleets) <= 1:
                    continue
                fleet_to_keep = fleets[0]
                for fleet_removed in fleets[1:]:
                    for ship_kept, ship_removed in zip(
                        fleet_to_keep.ships, fleet_removed.ships
                    ):
                        ship_kept.components[
                            ShipComponent
                        ].number += ship_removed.components[ShipComponent].number
                        ship_removed.components[ShipComponent].number = 0

            # Delete empty fleets
            fleets_to_delete = []
            for i, fleet in enumerate(player.fleets):
                to_delete = True
                for ship in fleet.ships:
                    if ship.components[ShipComponent].number > 0:
                        to_delete = False
                if to_delete:
                    fleets_to_delete.append(i)
            for i in fleets_to_delete[::-1]:
                fleet = player.fleets.pop(i)
                fleet.destruct()
                for ship in fleet.ships:
                    ship.destruct()
                    del ship
                del fleet

    def execute_mission(self, game_state: GameState, fleet: Fleet):
        fleet_comp = fleet.components[FleetComponent]
        if fleet_comp.mission == "TRANSPORT":
            destination_planet = game_state.world.planets[fleet_comp.travelling_to]
            dest_planet_comp = destination_planet.components[PlanetComponent]
            dest_planet_comp.resources = add_resources(
                dest_planet_comp.resources, fleet_comp.cargo
            )
            fleet_comp.cargo = empty_resources()

            fleet_comp.mission = "RETURN"
            prev_destination = fleet_comp.travelling_to
            fleet_comp.travelling_to = fleet_comp.travelling_from
            fleet_comp.travelling_from = prev_destination

            fleet_comp.travel_time_total = self.compute_travelling_time(
                game_state, fleet, fleet_comp.travelling_from, fleet_comp.travelling_to,
            )

            fleet_comp.travel_time_left = fleet_comp.travel_time_total

        elif fleet_comp.mission == "RETURN":
            destination_planet = game_state.world.planets[fleet_comp.travelling_to]
            dest_planet_comp = destination_planet.components[PlanetComponent]
            dest_planet_comp.resources = add_resources(
                dest_planet_comp.resources, fleet_comp.cargo
            )
            fleet_comp.cargo = empty_resources()

            fleet_comp.current_location = fleet_comp.travelling_to
            fleet_comp.in_transit = False
            fleet_comp.travelling_to = (
                fleet_comp.travelling_from
            ) = (
                fleet_comp.mission
            ) = fleet_comp.travel_time_total = fleet_comp.travel_time_left = 0

        elif fleet_comp.mission == "COLONIZE":
            if not PositionSystem.is_location_free(fleet_comp.travelling_to):
                self.finish_mission_and_return(fleet)
            else:
                # Remove one colony ship
                fleet.colony_ship.components[ShipComponent].number -= 1
                # Create new planet
                planet_id = fleet_comp.travelling_to
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
                    planet_comp.resources, fleet_comp.cargo
                )
                fleet_comp.cargo = empty_resources()

                # Fleet stays at new planet
                self.stop_fleet(fleet)
        elif fleet_comp.mission == "ATTACK":
            defender_planet = game_state.world.planets[fleet_comp.travelling_to]
            defender_id = defender_planet.components[PlanetComponent].owner_id
            # we find the defender fleet if there is one
            defender_fleet = None
            for defender_fleet in game_state.players[defender_id].fleets:
                defender_fleet_comp = defender_fleet.components[FleetComponent]
                if (
                    not defender_fleet_comp.in_transit
                    and defender_fleet_comp.current_location == fleet_comp.travelling_to
                ):
                    break
            combat_log = CombatSystem.resolve_combat(
                defender_planet, defender_fleet, fleet
            )
            if combat_log.attacker_victory:
                # the fleet takes all the resources it can carry
                defender_planet_comp = defender_planet.components[PlanetComponent]
                loot = self._decide_loot(
                    defender_planet_comp.resources, fleet_comp.available_cargo,
                )
                defender_planet_comp.resources = subtract_cost(
                    defender_planet_comp.resources, loot
                )

                fleet_comp.cargo = add_resources(fleet_comp.cargo, loot)
                print(id(fleet_comp.cargo))
                self.finish_mission_and_return(fleet)

    def _decide_loot(
        self,
        resource_quantities: Dict[Resources, float],
        available_space: float,
        priority=RESOURCES_PRIORITY,
    ) -> Dict[Resources, float]:
        loot = {}
        for resource in priority:
            loot[resource] = min(resource_quantities[resource], available_space)
            available_space -= loot[resource]
        return loot

    def finish_mission_and_return(self, fleet: Fleet):
        fleet_comp = fleet.components[FleetComponent]
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
        fleet_comp = fleet.components[FleetComponent]
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
        fleet_comp = fleet.components[FleetComponent]
        ships = fleet.ships

        fleet_speed = min([ship.components[ShipComponent].speed for ship in ships])

        total_distance = fleet_comp.travelling_from.distance_from(
            fleet_comp.travelling_to
        )
        travelling_time = 10 + 35 * math.sqrt(10 * total_distance / fleet_speed) / SPEED

        return travelling_time

    def get_planet_fleet(self, player_id: str, planet_id: PlanetLocation) -> Fleet:
        """
        Returns None if no fleet was found at this planet
        """
        game_state: GameState = EntityCatalog.get_special("game_state")

        assert player_id in game_state.players
        player = game_state.players[player_id]

        for fleet in player.fleets:
            fleet_comp = fleet.components[FleetComponent]
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

        fleet_comp = fleet.components[FleetComponent]

        assert (
            not fleet_comp.in_transit
        ), "Cannot assign mission to fleet already in transit"
        assert mission in VALID_MISSIONS, f"Invalid mission: {mission}"

        if mission != "COLONIZE":
            assert (
                destination_id in game_state.world.planets
            ), f"Cannot find planet id {destination_id}"

        if mission == "ATTACK":
            destination_owner_id = (
                game_state.world.planets[destination_id]
                .components[PlanetComponent]
                .owner_id
            )
            assert (
                fleet.owner_id != destination_owner_id
            ), "Cannot attack your own planet"

        planet_from = game_state.world.planets[fleet_comp.current_location]
        planet_comp = planet_from.components[PlanetComponent]
        if not sufficient_funds(cargo, planet_comp.resources):
            raise MissionException("Insufficient resources on planet")

        if sum(cargo.values()) > fleet_comp.available_cargo:
            raise MissionException("Insufficient cargo storage on your fleet")

        planet_comp.resources = subtract_cost(cargo, planet_comp.resources)
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
