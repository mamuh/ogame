from typing import Dict, List

import requests

server_url = "http://localhost:5000"


def get_state() -> Dict:
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


def run():
    running = server_is_running()

    if not running:
        print("Server is down...")
        return

    print("Server is running.")

    choice = ask_for_options(["Login", "New Player"])

    if choice == "Login":
        print("Enter you name")
        player_name = input()

    else:
        success = False
        while not success:
            print("Pick your username")
            player_name = input()
            success = create_player(player_name)
            if not success:
                print("Invalid user name. Try again")

    print("You are now logged in.")


if __name__ == "__main__":
    run()
