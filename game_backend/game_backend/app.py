#!/usr/bin/env python3

from flask import Flask

from game_backend.game import Game
from game_backend.init_game import initialise_gamestate


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/get_state")
def get_state():
    return game_state.to_json()


if __name__ == "__main__":
    game_state = initialise_gamestate()
    game_thread = Game(game_state)

    game_thread.start()

    app.run()
