#!/usr/bin/env python3
import random

from game_backend.entities.entities import (
    GameState,
    World,
    Planet,
    Player,
)


def initialise_gamestate() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                "earth": Planet.new(
                    name="Earth",
                    planet_id="earth",
                    size=16,
                    position=4,
                    solar_system=1,
                    galaxy=1,
                    owner_id="max",
                )
            }
        ),
        players={"max": Player.new(id="max", name="Max")},
    )
    return game_state


def initialise_empty_universe(size: int) -> GameState:
    game_state = GameState(
        world=World(
            planets={
                f"planet_{i}": Planet.new(
                    name=f"Planet_{i}",
                    planet_id=f"planet_{i}",
                    size=random.randint(100, 300),
                    position=random.randint(1, 9),
                    solar_system=random.randint(1, 500),
                    galaxy=random.randint(1, 5),
                    owner_id=None,
                )
                for i in range(size)
            }
        ),
        players={},
    )
    return game_state
