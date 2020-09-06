#!/usr/bin/env python3

from enum import Enum
from typing import Dict


class Resources(Enum):
    Metal = "metal"
    Oil = "oil"


def sufficient_funds(
    cost: Dict[Resources, float], available: Dict[Resources, float]
) -> bool:
    for resource, quantity in cost.items():
        if quantity > available.get(resource, 0):
            return False
    return True


def subtract_cost(
    cost: Dict[Resources, float], available: Dict[Resources, float]
) -> Dict[Resources, float]:
    return {
        resource: available_quantity - cost.get(resource, 0)
        for resource, available_quantity in available.items()
    }


def add_resources(
    cargo_a: Dict[Resources, float], cargo_b: Dict[Resources, float]
) -> Dict[Resources, float]:
    return {
        resource: cargo_a.get(resource, 0) + cargo_b.get(resource, 0)
        for resource in set(cargo_a).union(set(cargo_b))
    }


def empty_resources() -> Dict[Resources, float]:
    return {resource: 0 for resource in Resources}
