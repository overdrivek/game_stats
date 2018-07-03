import pandas as pd
import os
import xlrd
import python_scripts.country_stats as cstat
import python_scripts.player_stats as pstat
class tippspiel:
    def __init__(self):
        file_name = os.path.normpath('../Data/world_cup_table.xlsx')
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

    def parse_games(self):
        for country in self.unique_countries:
            cst = cstat.country_stats(country=country, scores=self.original_scores)
            self.country_list[country] = cst

    def parse_players(self):
        for player in self.players:
            predicted_score = self.workbook.sheet_by_name(player)
            pst = pstat.player_stats(player_name = player,original_score=self.original_scores,predicted_score=predicted_score)
            self.player_list[player] = pst

if __name__ == '__main__':
    tipspiel_parser = tippspiel()