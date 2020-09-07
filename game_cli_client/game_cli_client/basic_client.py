from typing import Dict, List

import requests

server_url = "http://localhost:5000"

SHIPS = ["light_fighter", "heavy_fighter", "colony_ship"]
MISSIONS = ["RETURN", "TRANSPORT", "COLONIZE", "ATTACK"]


def get_game_state() -> Dict:
    game_state = requests.get(f"{server_url}/get_state")
    return game_state.json()


def create_player(player_id: str) -> bool:
    response = requests.post(f"{server_url}/new_player/{player_id}")
    success = (response.status_code == 200) & (response.text == "True")
    print(response.text)
    return success


def server_is_running() -> bool:
    response = requests.get(f"{server_url}/ping")
    return response.status_code == 200


def ask_for_options(options: List[str], default=None):
    possible_choices = []
    for i, option in enumerate(options):
        print(f"{i+1} - {option}")
        possible_choices.append(str(i + 1))

    invalid_input = True
    user_input = None
    while invalid_input:
        user_input = input()
        if user_input in possible_choices:
            invalid_input = False
        elif user_input == "" and default is not None:
            user_input = default + 1
            invalid_input = False
        else:
            print("Invalid input. Try again.")
    return options[int(user_input) - 1]


def get_player_data(player_id: str):
    return {
        "planets": get_player_planets(player_id),
        "fleets": get_player_fleets(player_id),
    }


def get_player_planets(player_id: str) -> Dict[str, Dict]:
    response = requests.get(f"{server_url}/player/{player_id}/get/planets")
    return response.json()


def get_player_fleets(player_id: str) -> List[Dict]:
    response = requests.get(f"{server_url}/player/{player_id}/get/fleets")
    return response.json()


def display_game_state(player_data, player_id: str):
    player_planets = player_data["planets"]
    player_fleets = player_data["fleets"]
    print()
    print("-" * 40)
    print("PLANETS")
    print("-" * 40)
    for planet_id, planet in player_planets.items():
        planet_comp = planet["components"]["PlanetComponent"]
        print(planet_comp["name"])
        resources_string = []
        for res in planet_comp["resources"]:
            resources_string.append(
                f"{res}: {int(planet_comp['resources'][res])}/{int(planet_comp['resources_storage'][res])}"
            )
        print("Resources:", " - ".join(resources_string))

        print("Buildings")
        for building_id, building in planet["buildings"].items():
            building_comp = building["components"]["BuildingComponent"]
            name = building_comp["name"]
            level = building_comp["level"]
            upgrade_cost = building_comp["upgrade_cost"]
            upgrade_cost_string = ", ".join(
                [f"{res}: {int(cost)}" for res, cost in upgrade_cost.items()]
            )
            building_string = (
                f"  - {name:20} - level {level} - Upgrade cost: {upgrade_cost_string}"
            )
            print(building_string)
        print()
    print()
    print("-" * 40)
    print("FLEETS")
    print("-" * 40)
    for fleet in player_fleets:
        fleet_comp = fleet["components"]["FleetPositionComponent"]
        in_transit = fleet_comp["in_transit"]
        if not in_transit:
            current_location = fleet_comp["current_location"]
            print(f"Location: {current_location}")
        else:
            travelling_from = fleet_comp["travelling_from"]
            travelling_to = fleet_comp["travelling_to"]
            print(
                f"Location: Deep Space. Travelling from: {travelling_from} to: {travelling_to}"
            )
        for ship in SHIPS:
            ship_number = fleet[ship]["components"]["ShipComponent"]["number"]
            if ship_number > 0:
                print(f"- {ship}: {ship_number}")
    print()


def upgrade_building(building_id: str, planet_id: str, player_id: str) -> bool:
    response = requests.post(
        f"{server_url}/player/{player_id}/actions/upgrade_building/{planet_id}/{building_id}"
    )
    return response.text == "True"


def build_ship(player_id: str, planet_id: str, ship_id: str) -> bool:
    response = requests.post(
        f"{server_url}/player/{player_id}/actions/build_ship/{planet_id}/{ship_id}"
    )
    return response.text == "True"


def send_mission(
    player_id: str,
    planet_id: str,
    mission: str,
    destination_id: str,
    cargo: Dict[str, str],
) -> bool:
    response = requests.post(
        f"{server_url}/player/{player_id}/actions/send_mission/{planet_id}/{mission}",
        json={"destination_id": destination_id, "cargo": cargo},
    )
    print(response)


def choose_planet(player_data):
    print("Pick a planet:")
    planet_id = ask_for_options(list(player_data["planets"].keys()))
    planet = player_data["planets"][planet_id]
    return planet_id, planet


def choose_building(planet):
    print("Pick a building:")
    building_id = ask_for_options(list(planet["buildings"].keys()))
    return building_id


def choose_ship():
    print("Pick a ship:")
    ship_id = ask_for_options(SHIPS)
    return ship_id


def choose_mission():
    print("Pick a mission:")
    mission = ask_for_options(MISSIONS)
    return mission


def run():
    running = server_is_running()

    if not running:
        print("Server is down...")
        return

    print("Server is running.")

    choice = ask_for_options(["Login", "New Player"])

    if choice == "Login":
        print("Enter you name")
        player_id = input()

    else:
        success = False
        while not success:
            print("Pick your username")
            player_id = input()
            success = create_player(player_id)
            if not success:
                print("Invalid user name. Try again")

    print(f"You are now logged in as {player_id}.")

    while True:
        player_data = get_player_data(player_id)
        display_game_state(player_data, player_id)
        choice = ask_for_options(
            ["Refresh", "Upgrade Building", "Build Ship", "Send Mission"], default=0,
        )

        if choice == "Refresh":
            continue
        elif choice == "Upgrade Building":
            planet_id, planet = choose_planet(player_data)
            building_id = choose_building(planet)
            upgrade_building(building_id, planet_id, player_id)
        elif choice == "Build Ship":
            planet_id, planet = choose_planet(player_data)
            ship_id = choose_ship()
            build_ship(player_id, planet_id, ship_id)
        elif choice == "Send Mission":
            planet_id, planet = choose_planet(player_data)
            mission = choose_mission()
            print("Enter destination")
            destination_id = input()
            planet_resources = planet["components"]["PlanetComponent"]["resources"]
            cargo = {}
            for resource in planet_resources:
                print(f"{resource} amount:")
                cargo[resource] = float(input())

            send_mission(player_id, planet_id, mission, destination_id, cargo)


if __name__ == "__main__":
    run()
