from dataclasses import dataclass
from threading import Thread
import time

from game_backend.config import TARGET_UPDATE_TIME
from game_backend.components import PlanetComponent, ProducerComponent, PlayerComponent
from game_backend.systems.production_system import ProductionSystem
from game_backend.entities.entities import Player


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
        ProductionSystem.update(dt)

    def action_upgrade_building(
        self, player_id: str, planet_id: str, building_id: str
    ) -> bool:
        assert player_id in self.game_state.players, f"Unknown player id {player_id}"
        assert (
            planet_id in self.game_state.world.planets
        ), f"Unknown planet id {planet_id}"
        assert (
            self.game_state.world.planets[planet_id]
            .components[PlanetComponent]
            .owner_id
            == player_id
        ), f"Player {player_id} does not own planet {planet_id}"
        return (
            self.game_state.world.planets[planet_id]
            .components[PlanetComponent]
            .upgrade_building(building_id)
        )

    def create_new_player(self, player_id: str, player_name: str) -> bool:
        if player_id in self.game_state.players:
            # Name is already taken...
            return False
        empty_planets = [
            planet.components[PlanetComponent]
            for planet in self.game_state.world.planets.values()
            if planet.components[PlanetComponent].owner_id is None
        ]
        if len(empty_planets) == 0:
            # No more space for a new player...
            return False
        self.game_state.players[player_id] = Player.new(id=player_id, name=player_name)
        empty_planets[0].owner_id = player_id
        return True

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
