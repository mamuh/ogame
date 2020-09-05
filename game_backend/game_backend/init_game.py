#!/usr/bin/env python3
import random

from game_backend.entities.entities import (
    GameState,
    World,
    Planet,
    Player,
)
from game_backend.entities.ships import Fleet


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


def init_state_complex() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                "earth": Planet.new(
                    name="Earth",
                    planet_id="earth",
                    size=250,
                    position=3,
                    solar_system=1,
                    galaxy=1,
                    owner_id="max",
                ),
                "mars": Planet.new(
                    name="Mars",
                    planet_id="mars",
                    size=200,
                    position=4,
                    solar_system=1,
                    galaxy=1,
                    owner_id="max",
                ),
            }
        ),
        players={"max": Player.new(id="max", name="Max")},
    )
    earth_fleet = Fleet.new("earth")
    earth_fleet.light_fighter.number = 10
    mars_fleet = Fleet.new("mars")
    mars_fleet.heavy_fighter.number = 5
    game_state.players["max"].fleets = [earth_fleet, mars_fleet]
    return game_state
