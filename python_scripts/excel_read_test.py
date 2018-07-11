import pandas as pd
import os
import xlrd
import python_scripts.country_stats as cstat
import python_scripts.player_stats as pstat
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import numpy as np
from scipy.stats import rankdata
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
        #self.plot_test()

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
            print("higest rank player after game {} is {}".format(game,player_names[rank_out[0]]))

    def plot_test(self):
        fig = plt.figure()
        #plt.subplot(3,1,1)
        for player_name in self.player_list:
            player= self.player_list[player_name]
            player_pts = player.exact_prediction_array
            #xnew = np.linspace(0,len(player_pts),100)
            #xvals = np.arange(0,len(player_pts))
            #ynew = spline(xvals,player_pts,xnew)
            plt.plot(range(len(player_pts)),player_pts,label=player.name)
            #plt.plot(xnew, ynew, label=player.name)
            plt.legend(loc='best')
            plt.grid(True)
            plt.xlabel('Game')
            plt.ylabel('# exact prediction')
        plt.show()

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

if __name__ == '__main__':
    tipspiel_parser = tippspiel()