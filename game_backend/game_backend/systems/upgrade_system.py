from typing import Dict, Tuple

from game_backend.components import (
    BuildingComponent,
    PlanetComponent,
    RequirementsComponent,
    ResearchComponent,
)
from game_backend.game_structs import PlanetLocation
from game_backend.ecs.entity import Entity, EntityCatalog
from game_backend.entities.entities import Player, Planet
from game_backend.entities.buildings import Building
from game_backend.resources import Resources


class UpgradeInsufficientFunds(Exception):
    pass


class UpgradeInsufficientRequirements(Exception):
    pass


class UpgradeSystem:
    def get_player_planet(
        self, player_id: str, planet_id: str
    ) -> Tuple[Player, Planet]:
        game_state = EntityCatalog.get_special("game_state")
        assert player_id in game_state.players
        player = game_state.players[player_id]

        assert planet_id in game_state.world.planets
        planet = game_state.world.planets[planet_id]
        planet_component = planet.components[PlanetComponent]

        assert planet_component.owner_id == player_id
        return player, planet

    def upgrade_building(
        self, player_id: str, planet_id: PlanetLocation, building_name: str
    ):

        player, planet = self.get_player_planet(player_id, planet_id)
        planet_component = planet.components[PlanetComponent]
        assert (
            building_name in planet.buildings
        ), f"Invalid building name: {building_name}"

        building = planet.buildings[building_name]
        building_component = building.components[BuildingComponent]
        upgrade_cost = building_component.upgrade_cost

        if not self.check_requirements_met(player, planet, building):
            return False
        if not self.check_enough_resources(planet, upgrade_cost):
            return False

        for resource_str, cost in upgrade_cost.items():
            planet_component.resources[Resources(resource_str)] -= cost

        building_component.level += 1

        return True

    def upgrade_research(
        self, player_id: str, planet_id: PlanetLocation, research_name: str
    ):
        # TODO This whole part could be simplified if we had an upgrade component
        # you would only need a single upgrade method that you apply to any entities
        player, planet = self.get_player_planet(player_id, planet_id)
        planet_component = planet.components[PlanetComponent]
        assert planet_component.owner_id == player_id

        assert (
            research_name in player.research
        ), f"Invalid research name: {research_name}"

        research = player.research[research_name]
        research_component = research.components[ResearchComponent]
        upgrade_cost = research_component.upgrade_cost

        if not self.check_requirements_met(player, planet, research):
            return False
        if not self.check_enough_resources(planet, upgrade_cost):
            return False

        for resource_str, cost in upgrade_cost.items():
            planet_component.resources[Resources(resource_str)] -= cost

        research_component.level += 1

        return True

    def check_requirements_met(
        self,
        player: Player,
        planet: Planet,
        entity_checked: Entity,
        raises_exception=False,
    ) -> bool:
        """
        Raises exceptions when requirements are not met
        """
        if not RequirementsComponent in entity_checked.components:
            # entity has no requirements
            return True

        requirements_component = entity_checked.components[RequirementsComponent]

        for building_id, level in requirements_component.building.items():
            if (
                planet.buildings[building_id].components[BuildingComponent].level
                < level
            ):
                if raises_exception:
                    raise UpgradeInsufficientRequirements(
                        f"Building requirement {building_id} level {level} not met"
                    )
                return False

        for research_id, level in requirements_component.research.items():
            if player.research[research_id].components[ResearchComponent].level < level:
                if raises_exception:
                    raise UpgradeInsufficientRequirements(
                        f"Research requirement: {research_id} level {level} not met"
                    )
                return False

        return True

    def check_enough_resources(
        self, planet: Planet, upgrade_cost: Dict[str, float], raises_exception=False,
    ) -> bool:
        for resource_str, cost in upgrade_cost.items():
            if (
                cost
                > planet.components[PlanetComponent].resources[Resources(resource_str)]
            ):
                if raises_exception:
                    raise UpgradeInsufficientFunds(
                        f"Insufficient {resource_str}. Costs {cost}"
                    )
                return False
        return True


UpgradeSystem = UpgradeSystem()
