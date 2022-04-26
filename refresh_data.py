import pickle
import time

import games_stats_factory
from datetime import datetime, timedelta
from threading import Timer


class Game:
    def __init__(self, game_stats):
        self.game = game_stats
        self.comeback = game_stats.get_score_greatest_comeback()
        self.close_game = game_stats.get_score_close_game()
        self.best_teams = game_stats.get_score_best_teams()
        self.personal_performance = game_stats.get_score_personal_performance()
        self.high_game_rate = game_stats.get_score_game_rate()


def save_data():
    games_stats = games_stats_factory.get_games_stats()
    games = []
    for game in games_stats:
        games.append(Game(game))
    with open("games.pkl", "wb") as f:
        pickle.dump(games, f)
    print("refreshed")


def get_next_time():
    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x
    return delta_t.total_seconds()


if __name__ == "__main__":
    save_data()
    print("initial setup")
    # while True:
    #     time.sleep(get_next_time())
    #     save_data()
