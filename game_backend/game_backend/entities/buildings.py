#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict

from game_backend.ecs.entity import Entity
from game_backend.components import (
    BuildingComponent,
    ProducerComponent,
    StorageComponent,
    CombatComponent,
    RequirementsComponent,
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


def MetalMine() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Metal: 1}, energy_consumption=5
            ),
            BuildingComponent: BuildingComponent(
                name="MetalMine",
                base_cost={Resources.Metal: 10},
                upgrade_cost_factor=1.1,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def CristalMine() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Cristal: 0.5}, energy_consumption=6
            ),
            BuildingComponent: BuildingComponent(
                name="CristalMine",
                base_cost={Resources.Metal: 20},
                upgrade_cost_factor=1.2,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def DeuteriumSynthesizer() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Deuterium: 1}, energy_consumption=7
            ),
            BuildingComponent: BuildingComponent(
                name="DeuteriumSynthesizer",
                base_cost={Resources.Metal: 20, Resources.Cristal: 20},
                upgrade_cost_factor=1.3,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def SolarPlant() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={}, energy_consumption=0, energy_production=20
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


def CristalHangar() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="CristalHangar",
                base_cost={Resources.Metal: 8},
                upgrade_cost_factor=1.3,
            ),
            StorageComponent: StorageComponent(
                resources_storage={Resources.Cristal: 2}
            ),
        }
    )


def DeuteriumTank() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="DeuteriumTank",
                base_cost={Resources.Metal: 8, Resources.Cristal: 10},
                upgrade_cost_factor=1.3,
            ),
            StorageComponent: StorageComponent(
                resources_storage={Resources.Deuterium: 2}
            ),
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


def ResearchLab() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="ResearchLab",
                base_cost={
                    Resources.Metal: 50,
                    Resources.Cristal: 100,
                    Resources.Deuterium: 50,
                },
                upgrade_cost_factor=1.5,
            )
        }
    )


def MissileTurret() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="MissileTurret",
                base_cost={Resources.Metal: 2000},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=3800, shield=34, damage=152,),
            RequirementsComponent: RequirementsComponent(
                building={"ship_yard": 1}, research={}
            ),
        }
    )


def LaserTurret() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="LaserTurret",
                base_cost={Resources.Metal: 1500, Resources.Cristal: 500},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=3800, shield=42, damage=190),
            RequirementsComponent: RequirementsComponent(
                building={"ship_yard": 2}, research={"laser": 3}
            ),
        }
    )


def HeavyLaser() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="HeavyLaser",
                base_cost={Resources.Metal: 6000, Resources.Cristal: 2000},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=15200, shield=170, damage=475),
            RequirementsComponent: RequirementsComponent(
                building={"ship_yard": 4}, research={"energy": 3, "laser": 6}
            ),
        }
    )


def Buildings() -> Dict[str, Building]:
    return {
        "metal_mine": MetalMine(),
        "cristal_mine": CristalMine(),
        "deuterium_synthesizer": DeuteriumSynthesizer(),
        "solar_plant": SolarPlant(),
        "metal_hangar": MetalHangar(),
        "cristal_hangar": CristalHangar(),
        "deuterium_tank": DeuteriumTank(),
        "ship_yard": ShipYard(),
        "research_lab": ResearchLab(),
        "missile_turret": MissileTurret(),
        "laser_turret": LaserTurret(),
        "heavy_laser": HeavyLaser(),
    }
