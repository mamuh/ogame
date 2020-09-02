from dataclasses import dataclass, field
from typing import List, Dict

from game_backend.ecs.entity import Entity
from game_backend.components import (
    PlanetComponent,
    BuildingComponent,
    ProducerComponent,
    PlayerComponent,
    StorageComponent,
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


def Buildings() -> Dict[str, Building]:
    return {
        "mine": Mine(),
        "oil_rig": OilRig(),
        "solar_plant": SolarPlant(),
        "metal_hangar": MetalHangar(),
        "oil_tank": OilTank(),
    }


@dataclass
class Planet(Entity):
    buildings: Dict[str, Building] = field(default_factory=Buildings)

    @classmethod
    def new(
        cls, name: str, size: int, owner_id: str = None,
    ):
        return cls(
            components={
                PlanetComponent: PlanetComponent(
                    name=name, size=size, owner_id=owner_id
                )
            },
        )


@dataclass
class World(Entity):
    planets: Dict[str, Planet] = field(default_factory=dict)


@dataclass
class Player(Entity):
    @classmethod
    def new(cls, id: str, name: str):
        return cls(components={PlayerComponent: PlayerComponent(id=id, name=name)})


@dataclass
class GameState(Entity):
    world: World = field(default_factory=World)
    players: Dict[str, Player] = field(default_factory=dict)

    @property
    def catalog_key(self):
        return "game_state"
