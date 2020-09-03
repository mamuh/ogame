#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict

from game_backend.ecs.entity import Entity
from game_backend.components import (
    BuildingComponent,
    ProducerComponent,
    StorageComponent,
    CombatComponent,
)
from game_backend.resources import Resources


@dataclass
class Building(Entity):
    @classmethod
    def new(
        cls,
        building_component: BuildingComponent,
        producer_component: ProducerComponent,
    ):
        return cls(
            components={
                BuildingComponent: building_component,
                ProducerComponent: producer_component,
            }
        )


def Mine() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Metal: 1}, energy_consumption=5
            ),
            BuildingComponent: BuildingComponent(
                name="Mine",
                base_cost={Resources.Metal: 10},
                upgrade_cost_factor=1.1,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def OilRig() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Oil: 0.5}, energy_consumption=6
            ),
            BuildingComponent: BuildingComponent(
                name="OilRig",
                base_cost={Resources.Metal: 20},
                upgrade_cost_factor=1.2,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def SolarPlant() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={}, energy_consumption=0, energy_production=15
            ),
            BuildingComponent: BuildingComponent(
                name="SolarPlant",
                base_cost={Resources.Metal: 10},
                upgrade_cost_factor=1.1,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def MetalHangar() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="MetalHangar",
                base_cost={Resources.Metal: 5},
                upgrade_cost_factor=1.2,
            ),
            StorageComponent: StorageComponent(resources_storage={Resources.Metal: 30}),
        }
    )


def OilTank() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="OilTank", base_cost={Resources.Metal: 8}, upgrade_cost_factor=1.3,
            ),
            StorageComponent: StorageComponent(resources_storage={Resources.Oil: 2}),
        }
    )


def ShipYard() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="ShipYard",
                base_cost={Resources.Metal: 20},
                upgrade_cost_factor=1.3,
            ),
        }
    )


def MissileTurret() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="MissileTurret",
                base_cost={Resources.Metal: 50},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=100, shield=30, damage=30,),
        }
    )


def Buildings() -> Dict[str, Building]:
    return {
        "mine": Mine(),
        "oil_rig": OilRig(),
        "solar_plant": SolarPlant(),
        "metal_hangar": MetalHangar(),
        "oil_tank": OilTank(),
        "ship_yard": ShipYard(),
        "missile_turret": MissileTurret(),
    }
