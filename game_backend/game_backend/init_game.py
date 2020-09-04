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


def initialise_empty_universe() -> GameState:
    game_state = GameState(world=World(planets={}), players={},)
    return game_state
