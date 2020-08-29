from dataclasses import dataclass, field
from abc import ABC
from uuid import uuid4
from typing import Dict

from game_backend.ecs.component import Component

# TODO: garbage collection
@dataclass
class Entity(ABC):
    components: Dict[type, Component] = field(default_factory=dict)
    id: str = None
    _parent_id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        for component_type, component in self.components.items():
            component._entity_id = self.id
        # We set the parent id of all children
        for attr in self.__dict__.values():
            if isinstance(attr, Entity):
                attr._parent_id = self.id
            elif isinstance(attr, list) or isinstance(attr, set):
                for element in attr:
                    if isinstance(element, Entity):
                        element._parent_id = self.id
            elif isinstance(attr, dict):
                for element in attr.values():
                    if isinstance(element, Entity):
                        element._parent_id = self.id
        EntityCatalog.register(self)

    @property
    def parent(self):
        if self._parent_id is None:
            return
        return EntityCatalog.entities_index[self._parent_id]

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
