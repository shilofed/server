from games_stats_factory import *
import numpy as np
# from flaskServer import *
import matplotlib.pyplot as plt
import pickle


class Game:
    def __init__(self, game):
        self.game = game
        self.comeback = game.get_score_greatest_comeback()
        self.close_game = game.get_score_close_game()
        self.best_teams = game.get_score_best_teams()
        self.personal_performance = game.get_score_personal_performance()



if __name__ == '__main__':
    # games_stats = get_games_stats()
    # biggest_score = -np.inf
    # best_score = None
    # for game in games_stats:
    #     score = game.get_score()
    #     print(game.line_score.TEAM_CITY_NAME[0] + " " + game.line_score.TEAM_NICKNAME[0]
    #           + " vs "
    #           + game.line_score.TEAM_CITY_NAME[1] + " " + game.line_score.TEAM_NICKNAME[1]
    #           + " score: " + str(score))
    # print(get_best_game("Close game=2;Great comeback=2;Good teams=8;personal performance=5;"))

    dates = get_last_k_days(200)
    with open('dates.pkl', 'wb') as f:
        pickle.dump(dates, f)

    games = []
    comebacks = []
    close_games = []
    personal_performances = []
    best_teams = []
    with open('comebacks.pkl', 'wb') as f:
        pickle.dump(comebacks, f)
    with open('close_games.pkl', 'wb') as g:
        pickle.dump(close_games, g)
    with open('personal_performances.pkl', 'wb') as h:
        pickle.dump(personal_performances, h)
    with open('best_teams.pkl', 'wb') as j:
        pickle.dump(best_teams, j)
    with open('dates.pkl', 'rb') as d:
        dates = pickle.load(d)
    while len(dates) > 0:
        print(len(dates))
        date = dates[-1]
        with open('comebacks.pkl', 'rb') as f:
            comebacks = pickle.load(f)
        with open('close_games.pkl', 'rb') as g:
            close_games = pickle.load(g)
        with open('personal_performances.pkl', 'rb') as h:
            personal_performances = pickle.load(h)
            print(personal_performances)
        with open('best_teams.pkl', 'rb') as j:
            best_teams = pickle.load(j)

        games = get_games_stats(date)
        print(date)
        print("num of games", len(games))
        for g in games:
            game = Game(g)
            comebacks.append(game.comeback)
            close_games.append(game.close_game)
            personal_performances.append(game.personal_performance)
            best_teams.append(game.best_teams)

        with open('comebacks.pkl', 'wb') as f:
            pickle.dump(comebacks, f)
        with open('close_games.pkl', 'wb') as g:
            pickle.dump(close_games, g)
        with open('personal_performances.pkl', 'wb') as h:
            pickle.dump(personal_performances, h)
        with open('best_teams.pkl', 'wb') as j:
            pickle.dump(best_teams, j)
        dates = dates[:-1]
        with open('dates.pkl', 'wb') as d:
            pickle.dump(dates, d)


        # games.append(Game(game))


    # for game in games:



    print("comeback:", comebacks)
    print("close_games:", close_games)
    print("personal_performances:", personal_performances)
    print("best_teams:", best_teams)

    plt.hist(best_teams, bins=5)
    # plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
    plt.show()










    # for game in games_stats:
    #     score = game.get_score()
    #     print(game.line_score.TEAM_CITY_NAME[0] + " " + game.line_score.TEAM_NICKNAME[0]
    #           + " vs "
    #           + game.line_score.TEAM_CITY_NAME[1] + " " + game.line_score.TEAM_NICKNAME[1]
    #           + " score: " + str(score))
    #
    #     if score > biggest_score:
    #         biggest_score = score
    #         best_score = game
    # if best_score == None:
    #     print("no game last night")
    # else:
    #     print(best_score.line_score.TEAM_CITY_NAME[0] + " " + best_score.line_score.TEAM_NICKNAME[0]
    #           + " vs "
    #           + best_score.line_score.TEAM_CITY_NAME[1] + " " + best_score.line_score.TEAM_NICKNAME[1])
