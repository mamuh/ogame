from dataclasses import dataclass, field
from typing import List, Dict

from game_backend.ecs.entity import Entity
from game_backend.components import (
    PlanetComponent,
    PlayerComponent,
    PlanetPositionComponent,
)
from game_backend.resources import Resources
from game_backend.entities.buildings import Building, Buildings
from game_backend.entities.ships import Fleet


@dataclass
class Planet(Entity):
    buildings: Dict[str, Building] = field(default_factory=Buildings)

    @classmethod
    def new(
        cls,
        planet_id: str,
        name: str,
        size: int,
        position: int,
        solar_system: int,
        galaxy: int,
        owner_id: str = None,
    ):
        # HACK
        from game_backend.systems.position_system import PositionSystem

        planet = cls(
            components={
                PlanetComponent: PlanetComponent(
                    name=name, size=size, owner_id=owner_id
                ),
                PlanetPositionComponent: PlanetPositionComponent(
                    galaxy=galaxy, solar_system=solar_system, position=position
                ),
            },
        )
        PositionSystem.register_planet(planet_id, planet)
        return planet


@dataclass
class World(Entity):
    planets: Dict[str, Planet] = field(default_factory=dict)


@dataclass
class Player(Entity):
    fleets: List[Fleet] = field(default_factory=list)

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
