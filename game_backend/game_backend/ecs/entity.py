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
            self.id = str(uuid4())
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

    @property
    def catalog_key(self):
        return

    def add_component(self, component: Component) -> "Entity":
        component_type = type(component)
        component._entity_id = self.id
        assert (
            component_type not in self.components
        ), f"Entity already has a component of type {component_type}"
        self.components[component_type] = component
        return self

    def serialise(self) -> Dict:
        components_dict = {}
        for component_type, component in self.components.items():
            components_dict[component_type.__name__] = component.to_dict()
        entity_children = {}
        other_attributes = {}
        for attr_name, attr in self.__dict__.items():
            if isinstance(attr, Entity):
                entity_children[attr_name] = attr.serialise()
            elif isinstance(attr, list):
                entity_list = []
                for element in attr:
                    if isinstance(element, Entity):
                        entity_list.append(element.serialise())
                entity_children[attr_name] = entity_list
            elif isinstance(attr, set):
                entity_set = set()
                for element in attr:
                    if isinstance(element, Entity):
                        entity_set.add(element.serialise())
                entity_children[attr_name] = entity_set
            elif isinstance(attr, dict):
                if attr_name == "components":
                    continue
                entity_dict = {}
                for k, element in attr.items():
                    if isinstance(element, Entity):
                        entity_dict[k] = element.serialise()
                entity_children[attr_name] = entity_dict
            else:
                other_attributes[attr_name] = attr
        return dict(components=components_dict, **entity_children, **other_attributes)

    def deserialise(self, entity_dict: Dict):
        pass


class EntityCatalog:
    def __init__(self):
        self.entities_index = {}
        self.special_index = {}

    def get_special(self, key: str):
        return self.special_index.get(key)

    def register(self, entity: Entity):
        self.entities_index[entity.id] = entity
        if entity.catalog_key is not None:
            self.special_index[entity.catalog_key] = entity


EntityCatalog = EntityCatalog()
