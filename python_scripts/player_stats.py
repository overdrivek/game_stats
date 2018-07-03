import numpy as np
class player_stats:
    def __init__(self,player_name = None,original_score=None,predicted_score=None):
        if player_name is None or original_score is None or predicted_score is None:
            return

        self.name = player_name
        self.games_predicted_correct = 0
        self.total_games_predicted = 0
        self.total_games = 0
        self.correct_tendency = 0
        self.exact_prediction = 0
        self.corrent_gdiff = 0
        self.percentage_correct = 0
        self.percentage_exact = 0
        self.percentage_tend_correct = 0
        self.percentile_correct = 0
        self.percentile_exact = 0
        self.percentile_tend_correct = 0

        self.predicted = None
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

    def compute_performance(self):
        orig_scores = np.array([np.array(self.original_score.col_values(2)).T,np.array(self.original_score.col_values(3)).T]).T
        diff_ = orig_scores-self.predicted
        diff_games = diff_[:,0]-diff_[:,1]

        self.correct_tendency = len(np.where(diff_games==0)[0])
        self.total_games_predicted = len(np.where(np.isnan(diff_games) == False)[0])
        self.tendency_check(orig_scores)

        self.percentage_correct = (self.games_predicted_correct/self.total_games)*100.0
        self.percentage_exact = (self.exact_prediction/self.total_games)*100.0
        self.percentage_tend_correct = (self.correct_tendency/self.total_games)*100.0

        self.percentile_correct = (self.games_predicted_correct / self.total_games_predicted) * 100.0
        self.percentile_exact = (self.exact_prediction / self.total_games_predicted) * 100.0
        self.percentile_tend_correct = (self.correct_tendency / self.total_games_predicted) * 100.0




    def tendency_check(self,orig_scores):
        diff_goals = orig_scores[:,0]-orig_scores[:,1]
        diff_pgoals = self.predicted[:,0]-self.predicted[:,1]

        for orig_score,pred_score in zip(orig_scores,self.predicted):
            if orig_score[0]-orig_score[1] == pred_score[0]-pred_score[1]:
                if orig_score[0] == pred_score[0]  and orig_score[1] == pred_score[1]:
                    self.exact_prediction += 1
                self.games_predicted_correct += 1
            elif np.sign(orig_score[0]-orig_score[1])==np.sign(pred_score[0]-pred_score[1]):
                self.games_predicted_correct += 1

        #self.correct_tendency = len(np.where(diff_goals==diff_pgoals)[0])
