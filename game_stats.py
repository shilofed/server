from pandas import DataFrame as df
import numpy as np


class GameStats:

    def __init__(self, line_score: df, other_stats: df):
        self.line_score = line_score
        self.other_stats = other_stats

    def get_score(self):
        score = 0

        score += np.max(self.other_stats.LEAD_CHANGES) / 2  # number of times the lead changed hands

        if np.max(self.line_score.PTS_OT1) > 0:  # if was an over time
            score += 5
        if np.max(self.line_score.PTS_OT2) > 0:  # 2 overtimes
            score += 3

        first_wins_losses = self.line_score.TEAM_WINS_LOSSES[0].split("-")
        SECOND_wins_losses = self.line_score.TEAM_WINS_LOSSES[1].split("-")
        first_rate = int(first_wins_losses[0]) / (
                    int(first_wins_losses[0]) + int(first_wins_losses[1]))  # win rate of first team
        second_rate = int(SECOND_wins_losses[0]) / (
                    int(SECOND_wins_losses[0]) + int(SECOND_wins_losses[1]))  # win rate of second team
        score += (first_rate + second_rate) * 20  # add points for good teams

        final_score = self.line_score.PTS
        winner = np.argmax(final_score)
        turn_around = self.other_stats.LARGEST_LEAD[1 - winner]  # adds for comeback of winner
        score += turn_around / 5

        final_score_close = np.max(final_score) - np.min(final_score)
        score -= final_score_close / 3

        return score

    def get_score_best_teams(self):
        first_wins_losses = self.line_score.TEAM_WINS_LOSSES[0].split("-")
        SECOND_wins_losses = self.line_score.TEAM_WINS_LOSSES[1].split("-")
        first_rate = int(first_wins_losses[0]) / (
                    int(first_wins_losses[0]) + int(first_wins_losses[1]))  # win rate of first team
        second_rate = int(SECOND_wins_losses[0]) / (
                    int(SECOND_wins_losses[0]) + int(SECOND_wins_losses[1]))  # win rate of second team
        score = (first_rate + second_rate) * 20  # add points for good teams
        return score

    def get_score_close_game(self):
        score = 0
        final_score = self.line_score.PTS

        score += np.max(self.other_stats.LEAD_CHANGES) / 2  # number of times the lead changed hands

        if np.max(self.line_score.PTS_OT1) > 0:  # if was an over time
            score += 5
        if np.max(self.line_score.PTS_OT2) > 0:  # 2 overtimes
            score += 3
        final_score_close = np.max(final_score) - np.min(final_score)
        score -= final_score_close / 3
        # to add some check in game
        return score

    def get_score_greatest_comeback(self):
        final_score = self.line_score.PTS
        winner = np.argmax(final_score)
        turn_around = self.other_stats.LARGEST_LEAD[1 - winner]  # adds for comeback of winner
        score = turn_around
        return score

    # def get_score_personal_performance(self):

