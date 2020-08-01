from dataclasses import dataclass
from threading import Thread
import time

from game_backend.config import TARGET_UPDATE_TIME


@dataclass
class GameState:
    pass

class Game(Thread):

    def __init__(self):
        super().__init__()
        self.game_state = GameState()

    def get_state(self):
        return self.game_state

    def update(self, dt):
        pass

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
            if remaining_time > 0
                time.sleep(remaining_time)

            
