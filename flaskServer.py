import numpy as np
import requests
from flask import Flask
import games_stats_factory
import json
import game_stats


app = Flask(__name__)


@app.route("/<arg>")
def get_best_game(arg):
    # print(arg)
    games_stats = games_stats_factory.get_games_stats()
    biggest_score = -np.inf
    best_score = None
    for game in games_stats:
        score = -np.inf
        if arg == 'Great comeback':
            score = game.get_score_greatest_comeback()
        elif arg == 'Close game':
            score = game.get_score_close_game()
        elif arg == 'Good teams':
            score = game.get_score_best_teams()
        elif arg == 'Pick for me':
            score = game.get_score()
        elif arg == 'Bad game':
            score = -game.get_score()
        else:
            score = game.get_score()

        if score > biggest_score:
            biggest_score = score
            best_score = game
    json_response = {}
    if best_score is None:
        json_response["response_tag"] = -1
    else:
        json_response["response_tag"] = 1
        json_response["team_1_id"] = int(best_score.line_score.TEAM_ID[0])
        json_response["team_2_id"] = int(best_score.line_score.TEAM_ID[1])

    return json.dumps(json_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0')  # initialize server
