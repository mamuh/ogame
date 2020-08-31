from typing import Dict

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities import GameState
from game_backend.components import ProducerComponent, PlanetComponent, PlayerComponent


class ProductionSystem:
    def __init__(self):
        producer_components_index = Dict[str, ProducerComponent]

    def update(self, dt: float):
        game_state: GameState = EntityCatalog.get_special("game_state")
        for planet_id, planet in game_state.world.planets.items():
            planet_comp = planet.components[PlanetComponent]
            planet_owner = game_state.players[planet_comp.owner_id]
            owner_comp = planet_owner.components[PlayerComponent]
            for building in planet.buildings:
                # TODO: There should be a production system.
                # Producer components get registered in this system
                # and the system updated updates these components
                if ProducerComponent in building.components:
                    producer_component = building.components[ProducerComponent]
                    for resource, rate in producer_component.production_rate.items():
                        owner_comp.resources[resource] += rate * dt


ProductionSystem = ProductionSystem()
