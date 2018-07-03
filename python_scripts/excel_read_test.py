import pandas as pd
import os
import xlrd
import country_stats as cstat
class tippspiel:
    def __init__(self):
        file_name = os.path.normpath('C:/Users/naraya01/Google Drive/Colab Notebooks/world_cup_table.xlsx')
        workbook = xlrd.open_workbook(file_name)
        self.original_scores = workbook.sheet_by_name('Original_Score')
        self.country_list = dict()

        all_countries = self.original_scores.col_values(0)
        away_countries = self.original_scores.col_types(1)
        all_countries.append(away_countries)
        self.unique_countries = []
        for x in all_countries:
            if x not in self.unique_countries:
                self.unique_countries.append(x)

        self.parse_games()

    def parse_games(self):
        for country in self.unique_countries:
            cst = cstat.country_stats(country=country, scores=self.original_scores)
            self.country_list[country] = cst

if __name__ == '__main__':
    tipspiel_parser = tippspiel()