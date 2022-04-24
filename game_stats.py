from pandas import DataFrame as df
import numpy as np

s_comebacks = 5.3589203158319645
s_best_teams = 4.362217413275033
s_close_games = 7.384647929796666
s_personal_performances = 11.911523582204435

mean_best_teams = 20.058902979060605
mean_close_games = -3.515874770433119
mean_comebacks = 6.666666666666667
mean_personal_performances = 34.47330282227308

class GameStats:

    def __init__(self, line_score: df, other_stats: df, player_stats: df, play_by_play: df):
        self.line_score = line_score
        self.other_stats = other_stats
        self.player_stats = player_stats
        self.play_by_play = play_by_play

    def get_score(self):
        score = 0
        score += self.get_score_close_game()
        score += self.get_score_best_teams()
        score += self.get_score_greatest_comeback()
        score += self.get_score_personal_performance()

        return score

    def get_score_best_teams(self):
        first_wins_losses = self.line_score.TEAM_WINS_LOSSES[0].split("-")
        SECOND_wins_losses = self.line_score.TEAM_WINS_LOSSES[1].split("-")
        first_rate = int(first_wins_losses[0]) / (
                    int(first_wins_losses[0]) + int(first_wins_losses[1]))  # win rate of first team
        second_rate = int(SECOND_wins_losses[0]) / (
                    int(SECOND_wins_losses[0]) + int(SECOND_wins_losses[1]))  # win rate of second team
        score = (first_rate + second_rate) * 20  # add points for good teams
        return (score - mean_best_teams) / s_best_teams

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
        if final_score_close < 3:
            score += 2
        if final_score_close < 2:
            score += 3
        # to add some check in game
        Q1 = self.play_by_play[self.play_by_play.PERIOD == 1]
        Q1 = (Q1[Q1.SCORE > "0"])["SCOREMARGIN"].replace("TIE", 0).astype(int)
        Q1 = np.array(Q1)
        m1 = np.mean(np.abs(Q1))
        # Q1 = Q1[Q1.SCORE > "0"].SCOREMARGIN.astype(int)
        Q2 = self.play_by_play[self.play_by_play.PERIOD == 2]
        Q2 = (Q2[Q2.SCORE > "0"])["SCOREMARGIN"].replace("TIE", 0).astype(int)
        Q2 = np.array(Q2)
        m2 = np.mean(np.abs(Q2))
        Q3 = self.play_by_play[self.play_by_play.PERIOD == 3]
        Q3 = (Q3[Q3.SCORE > "0"])["SCOREMARGIN"].replace("TIE", 0).astype(int)
        Q3 = np.array(Q3)
        m3 = np.mean(np.abs(Q3))
        Q4 = self.play_by_play[self.play_by_play.PERIOD == 4]
        Q4 = (Q4[Q4.SCORE > "0"])["SCOREMARGIN"].replace("TIE", 0).astype(int)
        Q4 = np.array(Q4)
        m4 = np.mean(np.abs(Q4))
        margin_sum = (0.5 * m1 + 0.7 * m2 + 0.8 * m3 + m4) / 3
        # print("margin_sum", margin_sum)
        # add buzzer basket
        return (score - margin_sum / 3 - mean_close_games) / s_close_games

    def get_score_greatest_comeback(self):
        final_score = self.line_score.PTS
        winner = self.line_score.TEAM_ID[np.argmax(final_score)]
        arg = 0 if self.other_stats.TEAM_ID[0] == winner else 1
        turn_around = self.other_stats.LARGEST_LEAD[1 - arg]  # adds for comeback of winner
        score = turn_around
        return (score - mean_comebacks) / s_comebacks

    def get_score_personal_performance(self):  # to change
        first_team = self.player_stats[self.player_stats.TEAM_ID == self.player_stats.TEAM_ID[0]]
        second_team = self.player_stats[self.player_stats.TEAM_ID != self.player_stats.TEAM_ID[0]]
        score_first_team = 0
        score_second_team = 0
        for index, player in first_team.iterrows():
            if player.MIN is None:
                pass
            else:
                cur_score = int(player.PTS + player.AST + player.STL * 2 + player.BLK * 2 + player.REB / 2)
                score_first_team = np.max([score_first_team, cur_score - 20])
        for index, player in second_team.iterrows():
            if player.MIN is None:
                pass
            else:
                cur_score = int(player.PTS + player.AST + player.STL * 2 + player.BLK * 2 + player.REB / 2)
                score_second_team = np.max([score_second_team, cur_score - 20])
        return (np.max([0.75 * score_first_team + score_second_team, score_first_team + 0.75 * score_second_team]) - mean_personal_performances) / s_personal_performances


    def get_score_game_rate(self):

        return 0  #  to implement
