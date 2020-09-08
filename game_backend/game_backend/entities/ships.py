#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

from game_backend.ecs.entity import Entity
from game_backend.components import (
    ShipComponent,
    CombatComponent,
    FleetComponent,
)
from game_backend.resources import Resources
from game_backend.game_structs import PlanetLocation


@dataclass
class Ship(Entity):
    pass


def LightFighter() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="LightFighter",
                number=0,
                cost={Resources.Metal: 30, Resources.Cristal: 10,},
                speed=10,
                cargo=100,
            ),
            CombatComponent: CombatComponent(hp=100, shield=20, damage=20),
        }
    )


def HeavyFighter() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="HeavyFighter",
                number=0,
                cost={Resources.Metal: 100, Resources.Cristal: 30},
                speed=10,
                cargo=150,
            ),
            CombatComponent: CombatComponent(hp=250, shield=40, damage=50,),
        }
    )


def ColonyShip() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="ColonyShip",
                number=0,
                cost={Resources.Metal: 10, Resources.Cristal: 0},
                speed=20,
                cargo=500,
            ),
            CombatComponent: CombatComponent(hp=500, shield=50, damage=10),
        }
    )


@dataclass
class Fleet(Entity):
    owner_id: str = None
    light_fighter: Ship = field(default_factory=LightFighter)
    heavy_fighter: Ship = field(default_factory=HeavyFighter)
    colony_ship: Ship = field(default_factory=ColonyShip)

    @classmethod
    def new(cls, owner_id: str, planet_location: PlanetLocation):
        return cls(
            owner_id=owner_id,
            components={
                FleetComponent: FleetComponent(
                    current_location=planet_location,
                    in_transit=False,
                    travelling_to=None,
                    travelling_from=None,
                )
            },
        )

    @property
    def ships(self) -> List[Ship]:
        return [self.light_fighter, self.heavy_fighter, self.colony_ship]
