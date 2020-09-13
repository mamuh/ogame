#!/usr/bin/env python3
from typing import Dict

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities.entities import GameState
from game_backend.entities.ships import Fleet
from game_backend.resources import Resources, sufficient_funds, subtract_cost
from game_backend.components import (
    BuildingComponent,
    PlanetComponent,
    ShipComponent,
    FleetComponent,
)
from game_backend.game_structs import PlanetLocation


class ShipBuildingSystem:
    def build_ship(player_id: str, planet_id: PlanetLocation, ship_id: str) -> bool:
        game_state: GameState = EntityCatalog.get_special("game_state")

        player = game_state.players[player_id]
        planet = game_state.world.planets[planet_id]

        if planet.buildings["shipyard"].components[BuildingComponent].level == 0:
            return False

        # Finding the appropriate fleet
        planet_fleet = None
        for fleet in player.fleets:
            fleet_position_comp = fleet.components[FleetComponent]
            if (
                not fleet_position_comp.in_transit
                and fleet_position_comp.current_location == planet_id
            ):
                planet_fleet = fleet
                break
        if planet_fleet is None:
            planet_fleet = Fleet.new(player_id, planet_id)
            player.fleets.append(planet_fleet)

        assert hasattr(planet_fleet, ship_id), f"Invalid ship id: {ship_id}"
        ship = getattr(planet_fleet, ship_id)

        planet_component = planet.components[PlanetComponent]
        ship_cost = ship.components[ShipComponent].cost

        if not sufficient_funds(ship_cost, planet_component.resources):
            return False

        planet_component.resources = subtract_cost(
            ship_cost, planet_component.resources
        )

        # Add one ship to the fleet
        ship.components[ShipComponent].number += 1

        return True
