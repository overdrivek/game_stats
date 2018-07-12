import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
class player_stats:
    def __init__(self,player_name = None,original_score=None,predicted_score=None,country_stats=None):
        if player_name is None or original_score is None or predicted_score is None or country_stats is None:
            return

        self.name = player_name
        self.country_statlist = country_stats
        self.games_predicted_correct = 0
        self.total_games_predicted = 0
        self.total_games = 0
        self.correct_tendency = 0
        self.exact_prediction = 0

        self.correct_prediction_array = []
        self.exact_prediction_array = []
        self.points_array = []
        self.table_position = []

        self.percentage_correct = 0
        self.percentage_exact = 0
        self.percentage_tend_correct = 0
        self.percentile_correct = 0
        self.percentile_exact = 0
        self.percentile_tend_correct = 0

        self.number_hausfrau_tips = 0
        self.number_selfbelief_genius_tips = 0
        self.winning_team_tendency_list = dict()
        self.underdog_tendency_list = dict()
        self.prediction_team_tendency_list = dict()

        self.predicted = None
        self.orig_scores = None
        predicted_h =  np.empty(len(predicted_score.col_values(2)))
        predicted_a = np.empty(len(predicted_score.col_values(2)))

        self.total_games = len(predicted_score.col_values(2))

        for i, (val_h,val_a) in enumerate(zip(predicted_score.col_values(2),predicted_score.col_values(3))):
            predicted_h[i] = None
            if val_h != '':
                predicted_h[i] = val_h

            predicted_a[i] = None
            if val_a != '':
                predicted_a[i] = val_a

        self.predicted=np.array([predicted_h.T,predicted_a.T]).T
        self.original_score = original_score
        self.compute_performance()
        self.winning_team_tendency_list = OrderedDict(sorted(self.winning_team_tendency_list.items(), key=lambda x: x[1], reverse=True))
        self.underdog_tendency_list = OrderedDict(sorted(self.underdog_tendency_list.items(), key=lambda x: x[1], reverse=True))
        self.prediction_team_tendency_list = OrderedDict(sorted(self.prediction_team_tendency_list.items(), key=lambda x: x[1], reverse=True))

    def cumulate_tendency_list(self,game,tendency_list):
        teams = [game[0],game[1]]
        for team in teams:
            if team not in tendency_list:
                tendency_list[team] = 0
        return tendency_list

    def compute_performance(self):
        self.orig_scores = np.array([np.array(self.original_score.col_values(2)).T,np.array(self.original_score.col_values(3)).T]).T
        diff_ = self.orig_scores-self.predicted
        diff_games = diff_[:,0]-diff_[:,1]

        self.correct_tendency = len(np.where(diff_games==0)[0])
        self.total_games_predicted = len(np.where(np.isnan(diff_games) == False)[0])
        self.tendency_check()

        self.percentage_correct = (self.correct_prediction_array[-1]/self.total_games)*100.0
        self.percentage_exact = (self.exact_prediction/self.total_games)*100.0
        self.percentage_tend_correct = (self.correct_tendency/self.total_games)*100.0

        self.percentile_correct = (self.correct_prediction_array[-1]/ self.total_games_predicted) * 100.0
        self.percentile_exact = (self.exact_prediction / self.total_games_predicted) * 100.0
        self.percentile_tend_correct = (self.correct_tendency / self.total_games_predicted) * 100.0

        self.number_selfbelief_genius_tips = len(np.where(np.abs(diff_games) >= 4)[0])

    def tendency_check(self):

        exact_prediction_counter = 0
        game_prediction_counter = 0
        pts = 0
        for game_number,(orig_score,pred_score) in enumerate(zip(self.orig_scores,self.predicted)):
            game = self.original_score.row_values(game_number)
            self.winning_team_tendency_list = self.cumulate_tendency_list(game, self.winning_team_tendency_list)
            self.underdog_tendency_list = self.cumulate_tendency_list(game, self.underdog_tendency_list)
            self.prediction_team_tendency_list = self.cumulate_tendency_list(game, self.prediction_team_tendency_list)

            team_favoured = None
            if pred_score[0] > pred_score[1]:
                team_favoured = game[0]
            elif pred_score[1] > pred_score[0]:
                team_favoured = game[1]
            if team_favoured is not None:
                if self.country_statlist[team_favoured].is_underdog is True:
                    if team_favoured in self.underdog_tendency_list:
                        self.underdog_tendency_list[team_favoured] += 1

                self.prediction_team_tendency_list[team_favoured] += 1

            pt_type = None
            # score difference is correct
            if orig_score[0]-orig_score[1] == pred_score[0]-pred_score[1]:
                # prediction is spot on
                if orig_score[0] == pred_score[0]  and orig_score[1] == pred_score[1]:
                    self.exact_prediction += 1
                    exact_prediction_counter += 1
                    pt_type = 'Exact'
                else:
                    if pt_type is None:
                        pt_type = 'Tendency'
                if pred_score[0] > pred_score[1]:
                    self.winning_team_tendency_list[game[0]] += 1
                elif pred_score[0] < pred_score[1]:
                    self.winning_team_tendency_list[game[1]] += 1


                game_prediction_counter += 1

            elif np.sign(orig_score[0]-orig_score[1])==np.sign(pred_score[0]-pred_score[1]):
                self.games_predicted_correct += 1
                game_prediction_counter += 1
                pt_type='correct'

            if pt_type == 'Exact':
                pts += 4
            elif pt_type == 'Tendency':
                pts += 3
            elif pt_type == 'correct':
                pts += 2
            else:
                pts += 0

            if (pred_score[0] == 2 and pred_score[1] == 1) or (pred_score[0]==1 and pred_score[1]==2):
                self.number_hausfrau_tips += 1

            self.exact_prediction_array.append(exact_prediction_counter)
            self.correct_prediction_array.append(game_prediction_counter)
            self.points_array.append(pts)


        # plt.figure()
        # plt.plot(np.arange(1,self.total_games+1),self.exact_prediction_array)
        # plt.plot(np.arange(1, self.total_games+1), self.correct_prediction_array)
        # plt.grid(True)
        # plt.xlabel('Number of Games')
        # plt.ylabel('Number of correctness')
        # plt.show()
        #self.correct_tendency = len(np.where(diff_goals==diff_pgoals)[0])

    def get_data(self,data_str=''):
        if data_str == 'exact':
            return (self.exact_prediction_array,'Exact_predictions')
        elif data_str == 'correct':
            return (self.correct_prediction_array,'Correct_predictions')
        elif data_str == 'points':
            return (self.points_array,'Total_points')
        elif data_str == 'hf_tips':
            return (self.number_hausfrau_tips, 'Hausfrau/Hausmann_Tipp')
        elif data_str == 'table_pos':
            return (self.table_position,'Standing')
        elif data_str == 'selfbelief':
            return (self.number_selfbelief_genius_tips, 'Brave_tips')
        elif data_str == 'percentage_correct':
            return (self.percentage_correct,'Percentage_correct')
        elif data_str == 'winning_tendency':
            return (self.winning_team_tendency_list,'Preferred team')