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


@app.route("/new_player/<name>", methods=["POST"])
def new_player(name: str):
    return str(game_thread.create_new_player(name, name))


@app.route(
    "/player/<player_id>/actions/upgrade_building/<planet_id>/<building_id>",
    methods=["POST"],
)
def upgrade_building(player_id: str, planet_id: str, building_id: str):
    return str(game_thread.action_upgrade_building(player_id, planet_id, building_id))


if __name__ == "__main__":
    game_state = initialise_gamestate()
    game_thread = Game(game_state)

    game_thread.start()

    app.run()
