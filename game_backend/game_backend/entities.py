from dataclasses import dataclass, field
from typing import List, Dict

from game_backend.ecs.entity import Entity
from game_backend.components import (
    PlanetComponent,
    BuildingComponent,
    ProducerComponent,
    PlayerComponent,
)


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


@dataclass
class Planet(Entity):
    buildings: List[Building] = field(default_factory=list)

    @classmethod
    def new(
        cls,
        name: str,
        size: int,
        owner_id: str = None,
        buildings: List[Building] = None,
    ):
        buidings = buildings or []
        return cls(
            buildings=buildings,
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
