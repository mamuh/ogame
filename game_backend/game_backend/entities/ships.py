#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

from game_backend.ecs.entity import Entity
from game_backend.components import (
    ShipComponent,
    CombatComponent,
    FleetPositionComponent,
)
from game_backend.resources import Resources


@dataclass
class Ship(Entity):
    pass


def LightFighter() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="LightFighter",
                number=0,
                cost={Resources.Metal: 30, Resources.Oil: 10,},
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
                cost={Resources.Metal: 100, Resources.Oil: 30},
                speed=10,
                cargo=150,
            ),
            CombatComponent: CombatComponent(hp=250, shield=40, damage=50,),
        }
    )


@dataclass
class Fleet(Entity):
    light_fighter: Ship = field(default_factory=LightFighter)
    heavy_fighter: Ship = field(default_factory=HeavyFighter)

    @classmethod
    def new(cls, planet_id: str):
        return cls(
            components={
                FleetPositionComponent: FleetPositionComponent(
                    current_planet_id=planet_id,
                    in_transit=False,
                    travelling_to=None,
                    travelling_from=None,
                )
            }
        )

    def get_ships(self) -> List[Ship]:
        return [self.light_fighter, self.heavy_fighter]


ships_index = {"light_fighter": LightFighter, "heavy_fighter": HeavyFighter}
