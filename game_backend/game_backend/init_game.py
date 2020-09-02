#!/usr/bin/env python3
import random

from game_backend.entities import (
    GameState,
    World,
    Planet,
    Player,
    Mine,
    OilRig,
    SolarPlant,
)
from game_backend.components import (
    ProducerComponent,
    BuildingComponent,
)
from game_backend.resources import Resources


def initialise_gamestate() -> GameState:
    game_state = GameState(
        world=World(
            planets={"earth": Planet.new(name="Earth", size=16, owner_id="max",)}
        ),
        players={"max": Player.new(id="max", name="Max")},
    )
    return game_state


def initialise_empty_universe(size: int) -> GameState:
    game_state = GameState(
        world=World(
            planets={
                f"planet_{i}": Planet.new(
                    name=f"Planet_{i}", size=random.randint(10, 20), owner_id=None,
                )
                for i in range(size)
            }
        ),
        players={},
    )
    return game_state
