#!/usr/bin/env python3

from game_backend.game_model import (
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

from game_backend.game_data import Mine, OilRig


def initialise_gamestate() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                "earth": Planet(
                    id="earth",
                    name="Earth",
                    size=16,
                    buildings=[Mine(), OilRig(),],
                    owner_id="max",
                )
            }
        ),
        players={"max": Player(id="max", name="Max")},
    )

    return game_state
