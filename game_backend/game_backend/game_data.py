#!/usr/bin/env python3

from dataclasses import dataclass
from game_backend.entities import Building
from game_backend.components import (
    ProducerComponent,
    BuildingComponent,
    PlanetComponent,
)
from game_backend.resources import Resources


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
                production_rate={Resources.Oil: 0.01}, energy_consumption=6
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
            StorageComponent: StorageComponent(
                resources_storage={Resources.Metal: 1000}
            ),
        }
    )
