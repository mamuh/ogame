#!/usr/bin/env python3
from dataclasses import dataclass, field, astuple
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.ecs.component import Component
from game_backend.resources import Resources, empty_resources, add_resources
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


@dataclass
class ShipComponent(Component, JsonSchemaMixin):
    name: str
    number: int
    cost: Dict[Resources, float]
    speed: float
    cargo: float


@dataclass
class ResearchComponent(Component, JsonSchemaMixin):
    name: str
    level: int
    cost: Dict[Resources, float]
    upgrade_cost_factor: float

    @property
    def upgrade_cost(self) -> Dict[str, float]:
        return {
            resource.value: resource_base_cost * self.upgrade_cost_factor ** self.level
            for resource, resource_base_cost in self.cost.items()
        }


@dataclass
class RequirementsComponent(Component, JsonSchemaMixin):
    building: Dict[str, int]
    research: Dict[str, int]


@dataclass
class CombatComponent(Component, JsonSchemaMixin):
    hp: float
    shield: float
    damage: float


@dataclass
class FleetComponent(Component, JsonSchemaMixin):
    current_location: PlanetLocation
    in_transit: bool
    travelling_to: PlanetLocation
    travelling_from: PlanetLocation
    cargo: Dict[Resources, float] = field(default_factory=empty_resources)
    travel_time_total: float = None
    travel_time_left: float = None
    mission: str = None

    @property
    def available_cargo(self) -> float:
        fleet = self.entity
        total_available = sum(
            [ship.components[ShipComponent].cargo for ship in fleet.ships]
        )
        already_taken = sum(self.cargo.values())
        return total_available - already_taken


@dataclass
class ProducerComponent(Component, JsonSchemaMixin):
    production_rate: Dict[Resources, float]
    energy_consumption: int
    energy_production: int = 0


@dataclass
class StorageComponent(Component, JsonSchemaMixin):
    resources_storage: Dict[Resources, float]
    upgrade_storage_factor: float = 1.833


@dataclass
class PlanetComponent(Component, JsonSchemaMixin):
    name: str
    size: int
    location: PlanetLocation
    owner_id: str
    resources: Dict[Resources, float] = field(
        default_factory=lambda: {resource: 0.0 for resource in Resources}
    )
    _production_per_second: Dict[Resources, float] = field(
        default_factory=empty_resources
    )
    _resources_storage: Dict[Resources, float] = field(default_factory=empty_resources)

    @property
    def energy_production(self) -> float:
        energy_production = 0
        planet = self.entity
        for building in planet.buildings.values():
            if ProducerComponent in building.components:
                prod_comp = building.components[ProducerComponent]
                building_comp = building.components[BuildingComponent]
                energy_production += (
                    prod_comp.energy_production
                    * building_comp.level
                    * building_comp.upgrade_prod_factor ** building_comp.level
                )
        return energy_production

    @property
    def energy_consumption(self) -> float:
        energy_consumption = 0
        planet = self.entity
        for building in planet.buildings.values():
            if ProducerComponent in building.components:
                prod_comp = building.components[ProducerComponent]
                building_comp = building.components[BuildingComponent]
                energy_consumption += (
                    prod_comp.energy_consumption
                    * building_comp.level
                    * building_comp.upgrade_prod_factor ** building_comp.level
                )
        return energy_consumption

    @property
    def energy_ratio(self) -> float:
        energy_consumption = self.energy_consumption
        if energy_consumption == 0:
            return 1
        return min(1, self.energy_production / energy_consumption)


@dataclass
class PlayerComponent(Component, JsonSchemaMixin):
    name: str
    id: str
