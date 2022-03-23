import pickle

import games_stats_factory
from apscheduler.schedulers.blocking import BlockingScheduler


class Game:
    def __init__(self, game):
        self.game = game
        self.comeback = game.get_score_greatest_comeback()
        self.close_game = game.get_score_close_game()
        self.best_teams = game.get_score_best_teams()
        self.personal_performance = game.get_score_personal_performance()


def save_data():
    games_stats = games_stats_factory.get_games_stats()
    games = []
    for game in games_stats:
        games.append(Game(game))
    with open("games.gms", "wb") as f:
        pickle.dump(games, f)


if __name__ == "__main__":
    games_stats = games_stats_factory.get_games_stats()
    games = []
    for game in games_stats:
        games.append(Game(game))
    with open("games.gms", "wb") as f:
        pickle.dump(games, f)
    scheduler = BlockingScheduler()
    scheduler.add_job(save_data, 'interval', hours=3)
    scheduler.start()
