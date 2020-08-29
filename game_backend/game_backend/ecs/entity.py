from dataclasses import dataclass
from abc import ABC
from uuid import uuid4
from typing import Dict

from game_backend.ecs.component import Component


@dataclass
class Entity(ABC):
    components: Dict[type, Component]
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        for component_type, component in self.components.items():
            component._entity_id = self.id
        EntityCatalog.register(self)

    def add_component(self, component: Component) -> "Entity":
        component_type = type(component)
        component._entity_id = self.id
        assert (
            component_type not in self.components
        ), f"Entity already has a component of type {component_type}"
        self.components[component_type] = component
        return self

    def serialise(self) -> str:
        pass

    def deserialise(self, entity_string: str):
        pass


class EntityCatalog:
    def __init__(self):
        self.entities_index = {}

    def register(self, entity: Entity):
        self.entities_index[entity.id] = entity


EntityCatalog = EntityCatalog()
