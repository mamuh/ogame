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

            # First we compute the energy ratio of the planet
            planet_energy_production = 0
            planet_energy_consumption = 0
            for building in planet.buildings:
                building_comp = building.components[BuildingComponent]
                prod_comp = building.components[ProducerComponent]
                if ProducerComponent in building.components:
                    planet_energy_production += (
                        prod_comp.energy_production
                        * building_comp.upgrade_prod_factor ** building_comp.level
                    )
                    planet_energy_consumption += (
                        prod_comp.energy_consumption
                        * building_comp.upgrade_prod_factor ** building_comp.level
                    )
            energy_ratio = min(1, planet_energy_production / planet_energy_consumption)

            # Then we update the production
            for building in planet.buildings:
                if ProducerComponent in building.components:
                    prod_comp = building.components[ProducerComponent]
                    building_comp = building.components[BuildingComponent]
                    for resource, rate in prod_comp.production_rate.items():
                        planet_comp.resources[resource] += (
                            rate
                            * energy_ratio
                            * dt
                            * building_comp.upgrade_prod_factor ** building_comp.level
                        )


ProductionSystem = ProductionSystem()
