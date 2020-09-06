#!/usr/bin/env python3
from dataclasses import dataclass, field, astuple
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.ecs.component import Component
from game_backend.resources import Resources, empty_resources
from game_backend.game_structs import PlanetLocation


@dataclass
class BuildingComponent(Component, JsonSchemaMixin):
    name: str
    base_cost: Dict[Resources, float]
    upgrade_cost_factor: float
    upgrade_prod_factor: float = 1
    level: int = 0

    @property
    def upgrade_cost(self) -> Dict[str, float]:
        return {
            resource.value: resource_base_cost * self.upgrade_cost_factor ** self.level
            for resource, resource_base_cost in self.base_cost.items()
        }

    def can_upgrade(self, resources: Dict[Resources, float]) -> bool:
        for resource_str, cost in self.upgrade_cost.items():
            if cost > resources[Resources(resource_str)]:
                return False
        return True


@dataclass
class ShipComponent(Component, JsonSchemaMixin):
    name: str
    number: int
    cost: Dict[Resources, float]
    speed: float
    cargo: float


@dataclass
class CombatComponent(Component, JsonSchemaMixin):
    hp: float
    shield: float
    damage: float


@dataclass
class FleetPositionComponent(Component, JsonSchemaMixin):
    current_location: PlanetLocation
    in_transit: bool
    travelling_to: PlanetLocation
    travelling_from: PlanetLocation
    cargo: Dict[Resources, float] = field(default_factory=empty_resources)
    travel_time_total: float = None
    travel_time_left: float = None
    mission: str = None


@dataclass
class ProducerComponent(Component, JsonSchemaMixin):
    production_rate: Dict[Resources, float]
    energy_consumption: int
    energy_production: int = 0


@dataclass
class StorageComponent(Component, JsonSchemaMixin):
    resources_storage: Dict[Resources, float]
    upgrade_storage_factor: float = 2


@dataclass
class PlanetComponent(Component, JsonSchemaMixin):
    name: str
    size: int
    location: PlanetLocation
    owner_id: str
    resources: Dict[Resources, float] = field(
        default_factory=lambda: {resource: 0.0 for resource in Resources}
    )

    @property
    def energy_ratio(self) -> float:
        energy_production = 0
        energy_consumption = 0
        planet = self.entity
        for building in planet.buildings.values():
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
    def production_per_second(self) -> Dict[str, float]:
        produced_resources = {res.value: 0 for res in Resources}
        planet = self.entity
        for building in planet.buildings.values():
            if ProducerComponent in building.components:
                prod_comp = building.components[ProducerComponent]
                building_comp = building.components[BuildingComponent]
                for resource, rate in prod_comp.production_rate.items():
                    produced_resources[resource.value] += (
                        rate
                        * self.energy_ratio
                        * building_comp.upgrade_prod_factor ** building_comp.level
                    )
        return produced_resources

    @property
    def resources_storage(self) -> Dict[str, float]:
        resources_storage_dict = {res.value: 0 for res in Resources}
        planet = self.entity
        for building in planet.buildings.values():
            if StorageComponent in building.components:
                stor_comp = building.components[StorageComponent]
                building_comp = building.components[BuildingComponent]
                for resource, storage in stor_comp.resources_storage.items():
                    resources_storage_dict[resource.value] += (
                        storage
                        * stor_comp.upgrade_storage_factor ** building_comp.level
                    )
        return resources_storage_dict

    def upgrade_building(self, building_name: str) -> bool:
        """
        Returns a boolean indicating upgrade success or failure
        """
        planet = self.entity
        assert (
            building_name in self.entity.buildings
        ), f"Invalid building name: {building_name}"
        building_comp = self.entity.buildings[building_name].components[
            BuildingComponent
        ]

        if not building_comp.can_upgrade(self.resources):
            return False

        for resource_str, cost in building_comp.upgrade_cost.items():
            self.resources[Resources(resource_str)] -= cost

        building_comp.level += 1

        return True


@dataclass
class PlayerComponent(Component, JsonSchemaMixin):
    name: str
    id: str
