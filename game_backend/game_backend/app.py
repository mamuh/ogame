#!/usr/bin/env python3
import json

from flask import Flask, request

from game_backend.game import Game
from game_backend.init_game import initialise_gamestate


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/get_state")
def get_state():
    return json.dumps(game_state.serialise())


@app.route("/actions/upgrade_building/<planet_id>/<building_slot>", methods=["POST"])
def upgrade_building(planet_id: str, building_slot: int):
    return str(game_thread.action_upgrade_building(planet_id, int(building_slot)))


if __name__ == "__main__":
    game_state = initialise_gamestate()
    game_thread = Game(game_state)

    game_thread.start()

    app.run()
