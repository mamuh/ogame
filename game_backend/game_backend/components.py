#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.ecs.component import Component
from game_backend.resources import Resources


@dataclass
class BuildingComponent(Component, JsonSchemaMixin):
    name: str
    base_cost: Dict[Resources, float]
    upgrade_cost_factor: float
    upgrade_prod_factor: float = 1
    level: int = 0

    @property
    def upgrade_cost(self):
        return {
            resource: resource_base_cost * self.upgrade_cost_factor ** self.level
            for resource, resource_base_cost in self.base_cost.items()
        }


@dataclass
class ProducerComponent(Component, JsonSchemaMixin):
    production_rate: Dict[Resources, float]
    energy_consumption: int
    energy_production: int = 0


@dataclass
class PlanetComponent(Component, JsonSchemaMixin):
    name: str
    size: int
    owner_id: str
    resources: Dict[Resources, float] = field(
        default_factory=lambda: {resource: 0.0 for resource in Resources}
    )

    @property
    def energy_ratio(self):
        energy_production = 0
        energy_consumption = 0
        planet = self.entity
        for building in planet.buildings:
            if ProducerComponent in building.components:
                prod_comp = building.components[ProducerComponent]
                building_comp = building.components[BuildingComponent]
                energy_production += (
                    prod_comp.energy_production
                    * building_comp.upgrade_prod_factor ** building_comp.level
                )
                energy_consumption += (
                    prod_comp.energy_consumption
                    * building_comp.upgrade_prod_factor ** building_comp.level
                )
        return min(1, energy_production / energy_consumption)

    @property
    def production_per_second(self):
        produced_resources = {res: 0 for res in Resources}
        planet = self.entity
        for building in planet.buildings:
            if ProducerComponent in building.components:
                prod_comp = building.components[ProducerComponent]
                building_comp = building.components[BuildingComponent]
                for resource, rate in prod_comp.production_rate.items():
                    produced_resources[resource] += (
                        rate
                        * self.energy_ratio
                        * building_comp.upgrade_prod_factor ** building_comp.level
                    )
        return produced_resources


@dataclass
class PlayerComponent(Component, JsonSchemaMixin):
    name: str
    id: str
