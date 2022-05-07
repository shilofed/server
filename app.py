import pickle

import numpy as np
import requests
from flask import Flask
import games_stats_factory
import json
import game_stats
from refresh_data import Game
import ast

app = Flask(__name__)


@app.route("/predict/<arg>")
def predict(arg):
    try:
        with open("future_games.pkl", "rb") as f:
            future_games_teams = pickle.load(f)
        # future_games_teams = games_stats_factory.get_future_games_teams()  # move to the pickle
        json_response = {}
        if not future_games_teams:
            json_response["response_tag"] = -1
        else:  # to find the best future game
            json_response["response_tag"] = 1
            json_response["team_1_id"] = future_games_teams[0][0]
            json_response["team_2_id"] = future_games_teams[0][1]
        return json.dumps(json_response)
    except:
        return "Record not found", 400


@app.route("/yesterday/<arg>")
def get_best_game(arg):
    try:
        biggest_score = -np.inf
        pref = arg.split(";")
        pref = list(filter(bool, pref))
        pref_dict = {}
        for p in pref:
            cur_pref = p.split("=")
            pref_dict[cur_pref[0]] = cur_pref[1]
        best_score = None
        with open("games.pkl", "rb") as f:
            games = pickle.load(f)
        # games = [Game(game) for game in games_stats_factory.get_games_stats()]  # move to the pickle

        json_response = {}
        for game_class in games:
            score = 0
            if 'Great_comeback' in pref_dict:
                score += int(pref_dict['Great_comeback']) * game_class.comeback
            if 'Close_game' in pref_dict:
                score += int(pref_dict['Close_game']) * game_class.close_game
            if 'Good_teams' in pref_dict:
                score += int(pref_dict['Good_teams']) * game_class.best_teams
            if 'High_game_rate' in pref_dict:
                score += int(pref_dict['High_game_rate']) * game_class.high_game_rate
            if 'personal_performance' in pref_dict:
                score += int(pref_dict['personal_performance']) * game_class.personal_performance
            if score > biggest_score:
                biggest_score = score
                best_score = game_class.game
        if best_score is None:
            json_response["response_tag"] = -1
        else:
            json_response["response_tag"] = 1
            json_response["team_1_id"] = int(best_score.line_score.TEAM_ID[0])
            json_response["team_2_id"] = int(best_score.line_score.TEAM_ID[1])
        return json.dumps(json_response)
    except:
        return "Record not found", 400


@app.route("/")
def hello():
    return 'hello world'


if __name__ == "__main__":
    # app.debug = True
    app.run()  # initialize server
    # app.run(host='0.0.0.0')  # added to run sever on computer
