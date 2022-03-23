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
    print(arg)
    with open("games.gms", "rb") as f:
        games = pickle.load(f)
    biggest_score = -np.inf
    pref = arg.split(";")
    pref = list(filter(bool, pref))
    pref_dict = {}
    for p in pref:
        cur_pref = p.split("=")
        pref_dict[cur_pref[0]] = cur_pref[1]
    best_score = None
    for game_class in games:
        score = 0
        if 'Great comeback' in pref_dict:
            score += int(pref_dict['Great comeback']) * game_class.comeback
        if 'Close game' in pref_dict:
            score += int(pref_dict['Close game']) * game_class.close_game
        if 'Good teams' in pref_dict:
            score += int(pref_dict['Good teams']) * game_class.best_teams
        # if 'Pick for me' in pref_dict:
        #     score += int(pref_dict['Pick for me']) * game.get_score()
        if 'personal performance' in pref_dict:
            score += int(pref_dict['personal performance']) * game_class.personal_performance

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
    print("return")
    return json.dumps(json_response)


if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0')  # initialize server
