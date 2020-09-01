#!/usr/bin/env python3

from game_backend.entities import (
    GameState,
    World,
    Planet,
    Player,
)
from game_backend.components import (
    ProducerComponent,
    BuildingComponent,
)
from game_backend.resources import Resources

from game_backend.game_data import Mine, OilRig, SolarPlant


def initialise_gamestate() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                "earth": Planet.new(
                    name="Earth",
                    size=16,
                    owner_id="max",
                    buildings=[Mine(), OilRig(), SolarPlant()],
                )
            }
        ),
        players={"max": Player.new(id="max", name="Max")},
    )
    return game_state
