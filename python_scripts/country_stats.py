class country_stats:
    def __init__(self,country=None,scores=None):
        if country is None or scores is None:
            return

        self.name = country
        self.goals_scored = 0
        self.goals_conceded = 0
        self.points = 0
        self.seed = 0
        self.underdog_threshold = 20
        self.is_underdog = False
        number_of_registered_games = scores.nrows
        for game_number in range(scores.nrows):
            score = scores.row_values(game_number)
            valid_game = [i for i, data in enumerate(score) if data == self.name]
            if len(valid_game) > 0:
                self.goals_scored += int([score[2] if valid_game[0]==0 else score[3]][0])
                self.goals_conceded += int([score[3] if valid_game[0]==0 else score[2]][0])
                if valid_game[0] == 0 and (score[2]>score[3]):
                    self.points += 3
                elif valid_game[0] == 1 and (score[3]>score[2]):
                    self.points += 3
                elif score[3] == score[2]:
                    self.points += 1

            if score[4] == self.name:
                if self.seed == 0:
                    self.seed = game_number
                    if self.seed > self.underdog_threshold:
                        self.is_underdog = True




