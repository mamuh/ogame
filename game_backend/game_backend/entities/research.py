from dataclasses import dataclass, field
from typing import Dict

from game_backend.ecs.entity import Entity
from game_backend.components import ResearchComponent, RequirementsComponent
from game_backend.resources import Resources


def EnergyResearch() -> Entity:
    return Entity(
        components={
            ResearchComponent: ResearchComponent(
                name="Energy",
                level=0,
                cost={
                    Resources.Metal: 100,
                    Resources.Cristal: 200,
                    Resources.Deuterium: 50,
                },
                upgrade_cost_factor=2,
            ),
            RequirementsComponent: RequirementsComponent(
                building={"research_lab": 1}, research={}
            ),
        }
    )


def LaserResearch() -> Entity:
    return Entity(
        components={
            ResearchComponent: ResearchComponent(
                name="Laser",
                level=0,
                cost={Resources.Metal: 20, Resources.Cristal: 40,},
                upgrade_cost_factor=1.7,
            ),
            RequirementsComponent: RequirementsComponent(
                building={"research_lab": 2}, research={"energy": 2}
            ),
        }
    )


def CombustionDrive() -> Entity:
    return Entity(
        components={
            ResearchComponent: ResearchComponent(
                name="Combustion Drive",
                level=0,
                cost={Resources.Metal: 400, Resources.Deuterium: 600},
                upgrade_cost_factor=2.0,
            ),
            RequirementsComponent: RequirementsComponent(
                building={"research_lab": 1}, research={"energy": 1}
            ),
        }
    )


def ImpulseDrive() -> Entity:
    return Entity(
        components={
            ResearchComponent: ResearchComponent(
                name="Impulse Drive",
                level=0,
                cost={
                    Resources.Metal: 2000,
                    Resources.Cristal: 4000,
                    Resources.Deuterium: 600,
                },
                upgrade_cost_factor=2.0,
            ),
            RequirementsComponent: RequirementsComponent(
                building={"research_lab": 2}, research={"energy": 1}
            ),
        }
    )


def ArmourTech() -> Entity:
    return Entity(
        components={
            ResearchComponent: ResearchComponent(
                name="Armour Technology",
                level=0,
                cost={Resources.Metal: 1000},
                upgrade_cost_factor=2.0,
            ),
            RequirementsComponent: RequirementsComponent(
                building={"research_lab": 2}, research={}
            ),
        }
    )


def Research() -> Dict[str, Entity]:
    return {
        "energy": EnergyResearch(),
        "laser": LaserResearch(),
        "combustion_drive": CombustionDrive(),
        "impulse_drive": ImpulseDrive(),
        "armour_tech": ArmourTech(),
    }
