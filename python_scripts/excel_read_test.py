import pandas as pd
import os
import xlrd
import python_scripts.country_stats as cstat
import python_scripts.player_stats as pstat
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import numpy as np
from scipy.stats import rankdata
from sklearn.preprocessing import MinMaxScaler
class tippspiel:
    def __init__(self):
        file_name = os.path.normpath('..\\Data\\world_cup_table.xlsx')
        self.workbook = xlrd.open_workbook(file_name)
        self.original_scores = self.workbook.sheet_by_name('Original_Score')
        self.country_list = dict()
        self.players = self.workbook.sheet_names()[1:]
        self.player_list = dict()

        all_countries = self.original_scores.col_values(0)
        away_countries = self.original_scores.col_values(1)
        all_countries.extend(away_countries)
        self.unique_countries = []
        for x in all_countries:
            if x not in self.unique_countries:
                self.unique_countries.append(x)

        self.parse_games()
        self.parse_players()
        self.order_positions()
        self.run_spurious()
        self.plot_test()

    def parse_games(self):
        for country in self.unique_countries:
            cst = cstat.country_stats(country=country, scores=self.original_scores)
            self.country_list[country] = cst

    def parse_players(self):
        for player in self.players:
            predicted_score = self.workbook.sheet_by_name(player)
            try:
                pst = pstat.player_stats(player_name = player,original_score=self.original_scores,predicted_score=predicted_score,country_stats=self.country_list)
                self.player_list[player] = pst
            except:
                pass

    def order_positions(self):
        point_arrays = None
        total_games = 0
        player_names = []
        for player in self.players:
            if point_arrays is None:
                point_arrays = np.array(self.player_list[player].points_array)
            else:
                point_arrays = np.vstack([point_arrays,np.array(self.player_list[player].points_array)])
            player_names.append(self.player_list[player].name)

        total_games = self.original_scores.nrows
        # get rank
        print('sorting')
        rank_matrix = None
        for game in range(total_games):
            points = point_arrays[:,game]

            rank_out = rankdata(-1*points, method='dense')
            if rank_matrix is None:
                rank_matrix = np.array(rank_out).transpose()
            else:
                rank_matrix = np.vstack([rank_matrix,np.array(rank_out).transpose()])
        for i,player in enumerate(self.players):
            self.player_list[player].table_position  = rank_matrix[:,i]



    def plot_test(self):

        #plt.subplot(3,1,1)
        for player in self.players:
             data,data_str = self.player_list[player].get_data('spurious_dax')

        # plt.subplot(3,1,2)
        # for player_name in self.player_list:
        #     player= self.player_list[player_name]
        #     player_pts = player.correct_prediction_array
        #     plt.plot(range(len(player_pts)),player_pts,label=player.name)
        #     #plt.legend()
        #     plt.grid(True)
        #     plt.xlabel('Game')
        #     plt.ylabel('# correct prediction')
        # plt.show()
    def run_spurious(self):
        pd_dax = pd.read_csv('..\\Data\\Spurious_1_DAX.csv')
        closing_dax = pd_dax.iloc[:,4]
        pd_temp = pd.read_csv('..\\Data\\spurious_weather_info.csv', sep=';')
        max_temp = pd_temp.iloc[:, 9]
        #plt.figure()
        for i,player in enumerate(self.players):
            table_post = self.player_list[player].table_position

            closing_dax_scaled,table_pos_scaled,corr_coeff_dax = self.get_interp(ref_series=closing_dax,act_series=table_post)
            self.player_list[player].closing_dax_scaled = closing_dax_scaled
            self.player_list[player].table_position_scaled = table_pos_scaled
            self.player_list[player].dax_corrcoeff = corr_coeff_dax[0,1]

            max_temp_scaled, table_pos_scaled, corr_coeff_temp = self.get_interp(ref_series=max_temp,act_series=table_post)

            self.player_list[player].max_temp_scaled = max_temp_scaled
            self.player_list[player].temp_corrcoeff = corr_coeff_temp[0, 1]

    def get_interp(self,ref_series=None,act_series=None):
        xvals = np.linspace(0, len(ref_series), len(act_series))
        x = np.linspace(0, len(ref_series), len(ref_series))
        ref_ip = np.interp(xvals, x, ref_series)
        corr_coeff = np.corrcoef(ref_ip , act_series)
        # print(np.array(closing_dax))
        # print(np.array(pts_array))

        scaler = MinMaxScaler()
        ref_scaled = scaler.fit_transform(ref_ip .reshape(-1, 1))
        scaler = MinMaxScaler()
        act_scaled = 1 - (scaler.fit_transform(np.array(act_series).reshape(-1, 1)))

        return ref_scaled,act_scaled,corr_coeff

if __name__ == '__main__':
    tipspiel_parser = tippspiel()
