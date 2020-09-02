#!/usr/bin/env python3
from dataclasses import dataclass

from game_backend.ecs.entity import Entity
from game_backend.components import ShipComponent
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
                hp=100,
                shield=20,
                damage=20,
                speed=10,
                cargo=100,
            )
        }
    )


def HeavyFighter() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="HeavyFighter",
                cost={Resources.Metal: 100, Resources.Oil: 30},
                hp=250,
                shield=40,
                damage=50,
                speed=10,
                cargo=150,
            )
        }
    )
