#!/usr/bin/env python3
import json

from flask import Flask, request

from game_backend.game import Game
from game_backend.init_game import initialise_gamestate


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/ping")
def ping():
    return "pong"


@app.route("/get_state")
def get_state():
    return json.dumps(game_state.serialise())


@app.route("/new_player/<name>", methods=["POST"])
def new_player(name: str):
    return str(game_thread.create_new_player(name, name))


@app.route("/player/<player_id>/get/planets")
def get_player_planets(player_id: str):
    return json.dumps(
        {
            planet_id: planet.serialise()
            for planet_id, planet in game_thread.get_player_planets(player_id).items()
        }
    )


@app.route("/player/<player_id>/get/fleets")
def get_player_fleets(player_id: str):
    return json.dumps(
        [fleet.serialise() for fleet in game_thread.get_player_fleets(player_id)]
    )


@app.route(
    "/player/<player_id>/actions/upgrade_building/<planet_id>/<building_id>",
    methods=["POST"],
)
def upgrade_building(player_id: str, planet_id: str, building_id: str):
    return str(game_thread.action_upgrade_building(player_id, planet_id, building_id))


@app.route(
    "/player/<player_id>/actions/build_ship/<planet_id>/<ship_id>", methods=["POST"],
)
def build_ship(player_id: str, planet_id: str, ship_id: str):
    return str(game_thread.action_build_ship(player_id, planet_id, ship_id))


@app.route(
    "/player/<player_id>/actions/build_ship/<planet_id>/<ship_id>", methods=["POST"]
)
def build_ship(player_id: str, planet_id: str, ship_id: str):
    return str(game_thread.action_build_ship(player_id, planet_id, ship_id))


if __name__ == "__main__":
    game_state = initialise_gamestate()
    game_thread = Game(game_state)

    game_thread.start()

    app.run()
