#!/usr/bin/env python3

from game_backend.game_model import (
    GameState,
    World,
    Planet,
    Mine,
    ProducerComponent,
    UpgradableComponent,
    Player,
    Resources,
)


def initialise_gamestate() -> GameState:
    game_state = GameState(
        world=World(
            planets={
                "earth": Planet(
                    id="earth",
                    name="Earth",
                    size=16,
                    buildings=[
                        Mine(
                            producer_component=ProducerComponent(
                                production_rate={Resources.Metal: 1}
                            ),
                            upgradable_component=UpgradableComponent(
                                base_cost=100, upgrade_cost_factor=1.1
                            ),
                        )
                    ],
                )
            }
        ),
        players={"max": Player(id="max", name="Max")},
    )

    return game_state
