#!/usr/bin/env python3
import random

from game_backend.entities.entities import (
    GameState,
    World,
    Planet,
    Player,
)
from game_backend.entities.ships import Fleet
from game_backend.components import ShipComponent
from game_backend.game_structs import PlanetLocation


def initialise_gamestate() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                PlanetLocation(1, 1, 3): Planet.new(
                    name="Earth",
                    planet_id=PlanetLocation(1, 1, 3),
                    size=16,
                    location=PlanetLocation(position=4, system=1, galaxy=1),
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


def init_fast_empty() -> GameState:
    game_state = GameState(world=World(planets={}, speed=1000), players={},)
    return game_state


def init_state_complex() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                PlanetLocation(1, 1, 3): Planet.new(
                    name="Earth",
                    planet_id=PlanetLocation(1, 1, 3),
                    size=250,
                    location=PlanetLocation(position=3, system=1, galaxy=1),
                    owner_id="max",
                ),
                PlanetLocation(1, 1, 4): Planet.new(
                    name="Mars",
                    planet_id=PlanetLocation(1, 1, 4),
                    size=200,
                    location=PlanetLocation(position=4, system=1, galaxy=1),
                    owner_id="max",
                ),
                PlanetLocation(1, 1, 5): Planet.new(
                    name="Jupiter",
                    planet_id=PlanetLocation(1, 1, 5),
                    size=300,
                    location=PlanetLocation(1, 1, 5),
                    owner_id="bob",
                ),
            }
        ),
        players={
            "max": Player.new(id="max", name="Max"),
            "bob": Player.new(id="bob", name="Bob"),
        },
    )
    earth_fleet = Fleet.new("max", PlanetLocation(1, 1, 3))
    earth_fleet.light_fighter.components[ShipComponent].number = 10
    mars_fleet = Fleet.new("max", PlanetLocation(1, 1, 4))
    mars_fleet.heavy_fighter.components[ShipComponent].number = 5
    game_state.players["max"].fleets = [earth_fleet, mars_fleet]

    jupiter_fleet = Fleet.new("bob", PlanetLocation(1, 1, 5))
    jupiter_fleet.heavy_fighter.components[ShipComponent].number = 5

    game_state.players["bob"].fleets = [jupiter_fleet]

    return game_state
