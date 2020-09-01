from typing import Dict

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities import GameState
from game_backend.components import (
    ProducerComponent,
    PlanetComponent,
    PlayerComponent,
    BuildingComponent,
)


class ProductionSystem:
    def __init__(self):
        producer_components_index = Dict[str, ProducerComponent]

    def update(self, dt: float):
        game_state: GameState = EntityCatalog.get_special("game_state")
        for planet_id, planet in game_state.world.planets.items():
            planet_comp = planet.components[PlanetComponent]
            production_per_second = planet_comp.production_per_second

            for resource, resource_prod_per_sec in production_per_second.items():
                planet_comp.resources[resource] += resource_prod_per_sec * dt


ProductionSystem = ProductionSystem()
