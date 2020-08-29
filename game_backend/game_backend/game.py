from dataclasses import dataclass
from threading import Thread
import time

from game_backend.config import TARGET_UPDATE_TIME
from game_backend.components import PlanetComponent, ProducerComponent, PlayerComponent


@dataclass
class GameState:
    pass


class Game(Thread):
    def __init__(self, game_state=None):
        if game_state is None:
            game_state = GameState()
        super().__init__()
        self.game_state = game_state

    def get_state(self):
        return self.game_state

    def update(self, dt):
        # Production round
        for planet_id, planet in self.game_state.world.planets.items():
            planet_comp = planet.components[PlanetComponent]
            planet_owner = self.game_state.players[planet_comp.owner_id]
            owner_comp = planet_owner.components[PlayerComponent]
            for building in planet.buildings:
                # TODO: There should be a production system.
                # Producer components get registered in this system
                # and the system updated updates these components
                if ProducerComponent in building.components:
                    producer_component = building.components[ProducerComponent]
                    for resource, rate in producer_component.production_rate.items():
                        owner_comp.resources[resource] += rate * dt

    def run(self):
        last_update = time.time()
        game_step = 0

        while True:
            game_step += 1
            step_start = time.time()
            dt = step_start - last_update
            last_update = step_start

            self.update(dt)

            # Now we sleep so that each step is the same lenght
            post_update_time = time.time()
            dt_2 = post_update_time - step_start
            remaining_time = TARGET_UPDATE_TIME - dt_2
            if remaining_time > 0:
                time.sleep(remaining_time)
