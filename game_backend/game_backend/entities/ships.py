#!/usr/bin/env python3
from dataclasses import dataclass

from game_backend.ecs.entity import Entity
from game_backend.components import ShipComponent, CombatComponent
from game_backend.resources import Resources


@dataclass
class Ship(Entity):
    pass


def LightFighter() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="LightFighter",
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
                cost={Resources.Metal: 100, Resources.Oil: 30},
                speed=10,
                cargo=150,
            ),
            CombatComponent: CombatComponent(hp=250, shield=40, damage=50,),
        }
    )


ships_index = {"light_fighter": LightFighter, "heavy_fighter": HeavyFighter}
