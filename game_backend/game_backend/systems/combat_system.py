#!/usr/bin/env python3

from dataclasses import dataclass
import random

import numpy as np

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities.entities import Planet
from game_backend.entities.ships import Fleet
from game_backend.components import (
    FleetComponent,
    ShipComponent,
    CombatComponent,
    PlanetComponent,
    BuildingComponent,
)

random.seed(42)


@dataclass
class CombatLog:
    attacker_victory: bool


class CombatSystem:
    def resolve_combat(
        self, planet: Planet, fleet_defender: Fleet, fleet_attacker: Fleet
    ) -> CombatLog:
        game_state = EntityCatalog.get_special("game_state")
        planet_comp = planet.components[PlanetComponent]
        if fleet_defender is None:
            # we spawn an empty fleet. It will be garbage collected by the mission system
            fleet_defender = Fleet.new(planet_comp.owner_id, planet_comp.location,)
            game_state.players[planet_comp.owner_id].fleets.append(fleet_defender)

        attacking_fleet_combat_components = [
            ship.components[CombatComponent] for ship in fleet_attacker.ships
        ]
        attacking_fleet_numbers = [
            ship.components[ShipComponent].number for ship in fleet_attacker.ships
        ]

        defending_fleet_combat_components = [
            ship.components[CombatComponent] for ship in fleet_defender.ships
        ]
        defending_fleet_numbers = [
            ship.components[ShipComponent].number for ship in fleet_defender.ships
        ]

        defending_planet_buildings = [
            building_id
            for building_id, building in planet.buildings.items()
            if CombatComponent in building.components
        ]
        defending_planet_combat_components = [
            planet.buildings[building_id].components[CombatComponent]
            for building_id in defending_planet_buildings
        ]
        defending_planet_numbers = [
            planet.buildings[building_id].components[BuildingComponent].level
            for building_id in defending_planet_buildings
        ]

        # One fighting round
        while sum(attacking_fleet_numbers) > 0 and (
            sum(defending_fleet_numbers) > 0 or sum(defending_planet_numbers) > 0
        ):

            # simplified system

            attacker_total_damage = sum(
                combat_component.damage * number
                for combat_component, number in zip(
                    attacking_fleet_combat_components, attacking_fleet_numbers
                )
            )

            print(attacker_total_damage)

            defender_total_hp = sum(
                combat_component.hp * number
                for combat_component, number in zip(
                    defending_fleet_combat_components, defending_fleet_numbers
                )
            ) + sum(
                combat_component.hp * number
                for combat_component, number in zip(
                    defending_planet_combat_components, defending_planet_numbers
                )
            )

            attack_damage_ratio = attacker_total_damage / defender_total_hp

            defender_total_damage = sum(
                combat_component.damage * number
                for combat_component, number in zip(
                    defending_fleet_combat_components, defending_fleet_numbers
                )
            ) + sum(
                combat_component.hp * number
                for combat_component, number in zip(
                    defending_planet_combat_components, defending_planet_numbers
                )
            )

            attacker_total_hp = sum(
                combat_component.hp * number
                for combat_component, number in zip(
                    attacking_fleet_combat_components, attacking_fleet_numbers
                )
            )

            defense_damage_ratio = defender_total_damage / attacker_total_hp

            for i in range(len(defending_fleet_numbers)):
                defending_fleet_numbers[i] = update_numbers(
                    attack_damage_ratio, defending_fleet_numbers[i]
                )

            for i in range(len(defending_planet_numbers)):
                defending_planet_numbers[i] = update_numbers(
                    attack_damage_ratio, defending_planet_numbers[i]
                )

            for i in range(len(attacking_fleet_numbers)):
                attacking_fleet_numbers[i] = update_numbers(
                    defense_damage_ratio, attacking_fleet_numbers[i]
                )

        attacker_victory = True
        if sum(attacking_fleet_numbers) <= 0:
            attacker_victory = False

        for i, ship in enumerate(fleet_attacker.ships):
            ship.components[ShipComponent].number = attacking_fleet_numbers[i]

        for i, ship in enumerate(fleet_defender.ships):
            ship.components[ShipComponent].number = defending_fleet_numbers[i]

        for i, building_id in enumerate(defending_planet_buildings):
            planet.buildings[building_id].components[
                BuildingComponent
            ].level = defending_planet_numbers[i]

        return CombatLog(attacker_victory)


CombatSystem = CombatSystem()


def update_numbers(attack_ratio, n_ships):
    n_death = int((attack_ratio + (random.random() - 0.5) / 10) * n_ships) + (
        1 if random.random() < attack_ratio else 0
    )
    return max(0, min(n_ships, n_ships - n_death))
