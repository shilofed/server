import pytz
import time
from nba_api.stats.endpoints import scoreboardv2, boxscoresummaryv2, BoxScoreTraditionalV2, PlayByPlayV2
from nba_api.stats import endpoints
# from tabulate import tabulate
from datetime import datetime, timedelta
from game_stats import GameStats


def get_yesterday():
    """
    :return: the date of yesterday in format y-m-d (E.g. 2021-12-07)
    """
    days_delta = 1
    yesterday = datetime.now(pytz.timezone('US/Eastern')) - timedelta(days=days_delta)
    return yesterday.strftime("%Y-%m-%d")


def get_today():
    """
    :return: the date of yesterday in format y-m-d (E.g. 2021-12-07)
    """
    days_delta = 0
    today = datetime.now(pytz.timezone('US/Eastern')) - timedelta(days=days_delta)
    return today.strftime("%Y-%m-%d")


def get_last_k_days(k):
    """
    :return: the date of yesterday in format y-m-d (E.g. 2021-12-07)
    """
    days = []
    days_delta = 1
    if datetime.today().hour < 5:
        days_delta = 2
    for i in range(k):
        cur_day = datetime.today() - timedelta(days=days_delta)
        days.append(cur_day.strftime("%Y-%m-%d"))
        days_delta += 1
    return days


def get_games_ids_mult_days(games_dates):
    """
    :param games_date: date of the required games
    :return: list with the game_ids of the games that day
    """
    games_ids = []
    for games_date in games_dates:
        games = scoreboardv2.ScoreboardV2(game_date=games_date, day_offset='00')
        games_df = games.game_header.get_data_frame()
        games_df = games_df[games_df["GAME_STATUS_ID"] == 3]  # only finished games
        games_ids += [game_id for game_id in games_df["GAME_ID"]]
    return games_ids


def get_games_ids(games_date=get_yesterday()):
    """
    :param games_date: date of the required games
    :return: list with the game_ids of the games that day
    """
    games = scoreboardv2.ScoreboardV2(game_date=games_date, day_offset='00')
    games_df = games.game_header.get_data_frame()
    games_df = games_df[games_df["GAME_STATUS_ID"] == 3]  # only finished games
    games_ids = [game_id for game_id in games_df["GAME_ID"]]
    return games_ids


def get_games_stats(games_date=get_yesterday()):
    """
    :param games_date: date of the required games
    :return: list of GameStats
    """
    games_ids = get_games_ids(games_date)
    games_stats = []
    for game_id in games_ids:
        game_stats = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
        line_score = game_stats.line_score.get_data_frame()
        other_stats = game_stats.other_stats.get_data_frame()
        player_stats = BoxScoreTraditionalV2(game_id=game_id).player_stats.get_data_frame()
        play_by_play = PlayByPlayV2(game_id=game_id).play_by_play.get_data_frame()
        # box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
        # first_team_box = box_score.data_sets[0].get_data_frame()

        games_stats.append(GameStats(line_score, other_stats, player_stats, play_by_play))
    return games_stats


def get_future_games_ids(games_date=get_today()):
    """
    :param games_date: date of the required games
    :return: list with the game_ids of the games that day
    """
    games = scoreboardv2.ScoreboardV2(game_date=games_date, day_offset='00')
    games_df = games.game_header.get_data_frame()
    # games_df = games_df[games_df["GAME_STATUS_ID"] == 1]  # only games that did not start
    games_ids = [game_id for game_id in games_df["GAME_ID"]]
    return games_ids


def get_future_games_teams(games_date=get_today()):
    games_ids = get_future_games_ids(games_date)
    teams = []
    for game_id in games_ids:
        game_stats = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
        line_score = game_stats.line_score.get_data_frame()
        teams.append([int(line_score.TEAM_ID[0]), int(line_score.TEAM_ID[1])])
    return teams


def get_games_stats_mult_days(games_dates):
    game_stats = []
    for date in games_dates:
        game_stats += get_games_stats(date)
    return game_stats
