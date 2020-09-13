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
                production_rate={Resources.Metal: 30 / 3600}, energy_consumption=10
            ),
            BuildingComponent: BuildingComponent(
                name="Metal Mine",
                base_cost={Resources.Metal: 60, Resources.Cristal: 15},
                upgrade_cost_factor=1.5,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def CristalMine() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Cristal: 20 / 3600}, energy_consumption=10
            ),
            BuildingComponent: BuildingComponent(
                name="Cristal Mine",
                base_cost={Resources.Metal: 48, Resources.Cristal: 24},
                upgrade_cost_factor=1.6,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def DeuteriumSynthesizer() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(
                production_rate={Resources.Deuterium: 10 / 3600}, energy_consumption=20
            ),
            BuildingComponent: BuildingComponent(
                name="Deuterium Synthesizer",
                base_cost={Resources.Metal: 225, Resources.Cristal: 75},
                upgrade_cost_factor=1.5,
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
                name="Solar Plant",
                base_cost={Resources.Metal: 75, Resources.Cristal: 30},
                upgrade_cost_factor=1.5,
                upgrade_prod_factor=1.1,
            ),
        }
    )


def MetalHangar() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Metal Hangar",
                base_cost={Resources.Metal: 1000},
                upgrade_cost_factor=2.0,
            ),
            StorageComponent: StorageComponent(
                resources_storage={Resources.Metal: 10000}
            ),
        }
    )


def CristalHangar() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Cristal Hangar",
                base_cost={Resources.Metal: 500, Resources.Cristal: 250},
                upgrade_cost_factor=2.0,
            ),
            StorageComponent: StorageComponent(
                resources_storage={Resources.Cristal: 10000}
            ),
        }
    )


def DeuteriumTank() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Deuterium Tank",
                base_cost={Resources.Metal: 1000, Resources.Cristal: 1000},
                upgrade_cost_factor=2,
            ),
            StorageComponent: StorageComponent(
                resources_storage={Resources.Deuterium: 10000}
            ),
        }
    )


def Shipyard() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Shipyard",
                base_cost={
                    Resources.Metal: 400,
                    Resources.Cristal: 200,
                    Resources.Deuterium: 100,
                },
                upgrade_cost_factor=2.0,
            ),
        }
    )


def ResearchLab() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Research Lab",
                base_cost={
                    Resources.Metal: 200,
                    Resources.Cristal: 400,
                    Resources.Deuterium: 200,
                },
                upgrade_cost_factor=2.0,
            )
        }
    )


def MissileTurret() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Missile Turret",
                base_cost={Resources.Metal: 2000},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=3800, shield=34, damage=152,),
            RequirementsComponent: RequirementsComponent(
                building={"shipyard": 1}, research={}
            ),
        }
    )


def LaserTurret() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Laser Turret",
                base_cost={Resources.Metal: 1500, Resources.Cristal: 500},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=3800, shield=42, damage=190),
            RequirementsComponent: RequirementsComponent(
                building={"shipyard": 2}, research={"laser": 3}
            ),
        }
    )


def HeavyLaser() -> Building:
    return Building(
        components={
            BuildingComponent: BuildingComponent(
                name="Heavy Laser",
                base_cost={Resources.Metal: 6000, Resources.Cristal: 2000},
                upgrade_cost_factor=1.0,
            ),
            CombatComponent: CombatComponent(hp=15200, shield=170, damage=475),
            RequirementsComponent: RequirementsComponent(
                building={"shipyard": 4}, research={"energy": 3, "laser": 6}
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
        "shipyard": Shipyard(),
        "research_lab": ResearchLab(),
        "missile_turret": MissileTurret(),
        "laser_turret": LaserTurret(),
        "heavy_laser": HeavyLaser(),
    }
