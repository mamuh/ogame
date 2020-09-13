#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

from game_backend.ecs.entity import Entity
from game_backend.components import (
    ShipComponent,
    CombatComponent,
    FleetComponent,
    RequirementsComponent,
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
                cost={Resources.Metal: 3000, Resources.Cristal: 1000,},
                speed=12500,
                cargo=50,
            ),
            CombatComponent: CombatComponent(hp=4000, shield=10, damage=50),
            RequirementsComponent: RequirementsComponent(
                building={"shipyard": 1}, research={"combustion_drive": 1}
            ),
        }
    )


def HeavyFighter() -> Ship:
    return Ship(
        components={
            ShipComponent: ShipComponent(
                name="HeavyFighter",
                number=0,
                cost={Resources.Metal: 6000, Resources.Cristal: 4000},
                speed=10000,
                cargo=100,
            ),
            CombatComponent: CombatComponent(hp=10000, shield=25, damage=150,),
            RequirementsComponent: RequirementsComponent(
                building={"shipyard": 3},
                research={"armour_tech": 2, "impulse_drive": 2},
            ),
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
            RequirementsComponent: RequirementsComponent(
                building={"shipyard": 4}, research={"impulse_drive": 4}
            ),
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
