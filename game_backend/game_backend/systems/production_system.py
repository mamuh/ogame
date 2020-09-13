from typing import Dict

from game_backend.ecs.entity import EntityCatalog
from game_backend.entities.entities import GameState, Planet
from game_backend.resources import Resources, empty_resources
from game_backend.components import (
    ProducerComponent,
    PlanetComponent,
    PlayerComponent,
    BuildingComponent,
    StorageComponent,
)


class ProductionSystem:
    def __init__(self):
        producer_components_index = Dict[str, ProducerComponent]

    def update(self, dt: float):
        game_state: GameState = EntityCatalog.get_special("game_state")
        for planet_id, planet in game_state.world.planets.items():
            self.update_planet_production(game_state.world.speed, planet)
            self.update_planet_storage(planet)
            planet_comp = planet.components[PlanetComponent]
            production_per_second = planet_comp._production_per_second
            planet_storage = planet_comp._resources_storage

            for resource, resource_prod_per_sec in production_per_second.items():
                capacity_left = (
                    planet_storage[resource] - planet_comp.resources[resource]
                )
                if capacity_left <= 0:

                    # The planet is at or above capacity for this resource, it stops accumulating
                    continue
                planet_comp.resources[resource] += min(
                    resource_prod_per_sec * dt, capacity_left
                )

    def update_planet_production(self, universe_speed: float, planet: Planet):
        planet_component = planet.components[PlanetComponent]
        produced_resources = empty_resources()
        for building in planet.buildings.values():
            if ProducerComponent in building.components:
                prod_comp = building.components[ProducerComponent]
                building_comp = building.components[BuildingComponent]
                for resource, rate in prod_comp.production_rate.items():
                    produced_resources[resource] += rate * universe_speed + (
                        rate
                        * universe_speed
                        * building_comp.level
                        * planet_component.energy_ratio
                        * building_comp.upgrade_prod_factor ** building_comp.level
                    )
        planet_component._production_per_second = produced_resources

    def update_planet_storage(self, planet: Planet):
        resources_storage = empty_resources()
        for building in planet.buildings.values():
            if StorageComponent in building.components:
                stor_comp = building.components[StorageComponent]
                building_comp = building.components[BuildingComponent]
                for resource, storage in stor_comp.resources_storage.items():
                    resources_storage[resource] += (
                        storage
                        * stor_comp.upgrade_storage_factor ** building_comp.level
                    )
        planet.components[PlanetComponent]._resources_storage = resources_storage


ProductionSystem = ProductionSystem()
