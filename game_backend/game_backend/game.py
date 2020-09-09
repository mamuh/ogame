from dataclasses import dataclass
from threading import Thread
import time
import random
from typing import List, Dict

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.config import TARGET_UPDATE_TIME
from game_backend.components import PlanetComponent, ProducerComponent, PlayerComponent
from game_backend.systems.production_system import ProductionSystem
from game_backend.systems.ship_building_system import ShipBuildingSystem
from game_backend.systems.position_system import PositionSystem
from game_backend.systems.mission_system import (
    MissionSystem,
    MissionException,
    VALID_MISSIONS,
)
from game_backend.systems.upgrade_system import UpgradeSystem
from game_backend.entities.entities import GameState, Player, Planet
from game_backend.entities.ships import Fleet
from game_backend.resources import Resources
from game_backend.game_structs import PlanetLocation


@dataclass
class ActionOutcome(JsonSchemaMixin):
    success: bool
    reason: str = None


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
        MissionSystem.update(dt)

    def check_player_id(self, player_id: str):
        assert player_id in self.game_state.players, f"Unknown player id {player_id}"

    def check_planet_id(self, planet_id: PlanetLocation):
        assert (
            planet_id in self.game_state.world.planets
        ), f"Unknown planet id {planet_id}"

    def check_player_planet(self, player_id: str, planet_id: PlanetLocation):
        self.check_player_id(player_id)
        self.check_planet_id(planet_id)
        assert (
            self.game_state.world.planets[planet_id]
            .components[PlanetComponent]
            .owner_id
            == player_id
        ), f"Player {player_id} does not own planet {planet_id}"

    def get_player_planets(self, player_id: str) -> Dict[str, Planet]:
        self.check_player_id(player_id)
        planet_ids = PositionSystem.get_player_planets(player_id)
        return {
            planet_id: self.game_state.world.planets[planet_id]
            for planet_id in planet_ids
        }

    def get_player_fleets(self, player_id: str) -> List[Fleet]:
        self.check_player_id(player_id)
        fleets = self.game_state.players[player_id].fleets
        return fleets

    def action_upgrade_building(
        self, player_id: str, planet_id: PlanetLocation, building_id: str
    ) -> bool:
        self.check_player_planet(player_id, planet_id)
        return UpgradeSystem.upgrade_building(player_id, planet_id, building_id)

    def action_build_ship(
        self, player_id: str, planet_id: PlanetLocation, ship_id: str
    ) -> ActionOutcome:
        self.check_player_planet(player_id, planet_id)
        result = ShipBuildingSystem.build_ship(player_id, planet_id, ship_id)
        return ActionOutcome(success=result)

    def action_send_mission(
        self,
        player_id: str,
        planet_id: PlanetLocation,
        mission: str,
        destination_id: PlanetLocation,
        cargo: Dict[Resources, float] = None,
    ) -> ActionOutcome:
        self.check_player_planet(player_id, planet_id)
        # self.check_planet_id(destination_id)
        assert mission in VALID_MISSIONS

        fleet = MissionSystem.get_planet_fleet(player_id, planet_id)
        if fleet is None:
            return ActionOutcome(success=False, reason="No fleet at this planet")
        try:
            MissionSystem.order_mission(fleet, mission, destination_id, cargo)
        except MissionException:
            # ATM raised only when resources on planet are insufficient
            return ActionOutcome(
                success=False, reason="Insufficient resources at this planet"
            )
        return ActionOutcome(success=True)

    def create_new_player(self, player_id: str, player_name: str) -> bool:
        if player_id in self.game_state.players:
            # Name is already taken...
            print("name taken")
            return False
        free_location = PositionSystem.get_random_free_location()
        planet_name = f"planet-{free_location.galaxy}-{free_location.system}-{free_location.position}"
        new_planet = Planet.new(
            free_location,
            planet_name,
            random.randint(170, 210),
            location=free_location,
            owner_id=player_id,
        )
        self.game_state.world.planets[free_location] = new_planet
        self.game_state.players[player_id] = Player.new(id=player_id, name=player_name)
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
