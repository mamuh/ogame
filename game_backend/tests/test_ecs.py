#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, List

from game_backend.ecs.entity import Entity, EntityCatalog
from game_backend.ecs.component import Component


def test_ecs():
    @dataclass
    class HealthComponent(Component):
        hp: int = 10

    @dataclass
    class AttackComponent(Component):
        damage: int = 2

    ennemy = Entity(components={HealthComponent: HealthComponent(hp=5)}).add_component(
        AttackComponent()
    )

    assert ennemy.components[HealthComponent].entity == ennemy
    assert ennemy.components[HealthComponent].hp == 5
    assert ennemy.components[AttackComponent].entity == ennemy
    assert ennemy.components[AttackComponent].damage == 2

    @dataclass
    class CompositeEntity(Entity):
        simple_entities: List[Entity] = None

    my_composite_entity = CompositeEntity(
        simple_entities=[
            Entity(components={HealthComponent: HealthComponent()}),
            Entity(components={HealthComponent: HealthComponent(20)}),
        ]
    )

    assert my_composite_entity._parent_id is None
    assert my_composite_entity.simple_entities[0].parent == my_composite_entity
    assert my_composite_entity.simple_entities[1].parent == my_composite_entity
