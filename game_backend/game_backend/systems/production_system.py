from typing import Dict

from game_backend.components import ProducerComponent


class ProductionSystem:
    def __init__(self):
        producer_components_index = Dict[str, ProducerComponent]

    def update(self, dt: float):
        pass


ProductionSystem = ProductionSystem()
