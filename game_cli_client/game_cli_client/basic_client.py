from typing import Dict, List

import requests

server_url = "http://localhost:5000"


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


def ask_for_options(options: List[str]):
    possible_choices = []
    for i, option in enumerate(options):
        print(f"{i} - {option}")
        possible_choices.append(str(i))

    invalid_input = True
    user_input = None
    while invalid_input:
        user_input = input()
        if user_input in possible_choices:
            invalid_input = False
        else:
            print("Invalid input. Try again.")
    return options[int(user_input)]


def get_player_planets(game_state, player_id: str):
    player_planets = [
        planet_id
        for planet_id, planet in game_state["world"]["planets"].items()
        if planet["components"]["PlanetComponent"]["owner_id"] == player_id
    ]
    return player_planets


def display_game_state(game_state, player_id: str):
    player_planets = get_player_planets(game_state, player_id)
    print()
    print("Your Planets")
    for planet_id in player_planets:
        planet = game_state["world"]["planets"][planet_id]
        planet_comp = planet["components"]["PlanetComponent"]
        print(planet_comp["name"])
        print("Resources:")
        print(planet_comp["resources"])
        print("Buildings")
        print(
            {
                building["components"]["BuildingComponent"]["name"]: building[
                    "components"
                ]["BuildingComponent"]["level"]
                for building_id, building in planet["buildings"].items()
            }
        )
        print()
    print()
    print("Your Fleet")
    for fleet in game_state["players"][player_id]["fleets"]:
        print(fleet)


def upgrade_building(building_id: str, planet_id: str, player_id: str) -> bool:
    response = requests.post(
        f"{server_url}/player/{player_id}/actions/upgrade_building/{planet_id}/{building_id}"
    )
    return response.text == "True"


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
        game_state = get_game_state()
        display_game_state(game_state, player_id)
        choice = ask_for_options(["Refresh", "Upgrade Building"])

        if choice == "Refresh":
            continue
        elif choice == "Upgrade Building":
            print("Planet:")
            planet_id = ask_for_options(get_player_planets(game_state, player_id))
            print("Building to upgrade:")
            building_id = ask_for_options(
                [
                    "mine",
                    "oil_rig",
                    "solar_plant",
                    "metal_hangar",
                    "oil_tank",
                    "ship_yard",
                    "missile_turret",
                ]
            )
            upgrade_building(building_id, planet_id, player_id)


if __name__ == "__main__":
    run()
