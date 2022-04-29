import pickle

import numpy as np
import requests
from flask import Flask
import games_stats_factory
import json
import game_stats
import ast

app = Flask(__name__)


@app.route("/<arg>")
def get_best_game(arg):
    class Game:
        def __init__(self, game_stats):
            self.game = game_stats
            self.comeback = game_stats.get_score_greatest_comeback()
            self.close_game = game_stats.get_score_close_game()
            self.best_teams = game_stats.get_score_best_teams()
            self.personal_performance = game_stats.get_score_personal_performance()
            self.high_game_rate = game_stats.get_score_game_rate()
    # print(arg)
    # with open("games.gms", "rb") as f:
    #     games = pickle.load(f)
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

        # print("score= ", score)
        if score > biggest_score:
            biggest_score = score
            best_score = game_class.game
    json_response = {}
    if best_score is None:
        json_response["response_tag"] = -1
    else:
        json_response["response_tag"] = 1
        json_response["team_1_id"] = int(best_score.line_score.TEAM_ID[0])
        json_response["team_2_id"] = int(best_score.line_score.TEAM_ID[1])
    # print("biggest score = ", biggest_score)
    # print("return")
    return json.dumps(json_response)
    #return 'hello'


@app.route("/")
def hello():
    return 'hello worldfsfd'

if __name__ == "__main__":

    # app.debug = True
    app.run()  # initialize server
