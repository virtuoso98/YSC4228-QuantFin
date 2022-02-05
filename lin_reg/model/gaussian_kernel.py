from model.data_store import DataStore
from functools import reduce
import math

class GaussianKernel(DataStore):

    def __init__(self, x_raw = [], y_raw = [], num_folds = 10) -> None:
        super().__init__(x_raw, y_raw, num_folds)
        self.mse = []
        self.bandwidths = [(i + 1) * 0.1 for i in range(20)]
        self.optimal_h = None
        self.final_y_preds = []

    def calc_kernel(self, i, j, h) -> float:
        x_delta = (self.x_raw[i] - self.x_raw[j]) ** 2
        return math.exp(- x_delta / h)

    def find_best_mse(self, y_pred_and_mse):
        """Finds minimum mean squared error

        """
        return min(y_pred_and_mse, key = lambda tup: tup[1])

    def find_total_weight(self, x_test, train_idx, h) -> float:
        total_weight = 0
        for x_train in train_idx:
            total_weight += self.calc_kernel(x_test, x_train, h)
        return total_weight

    def get_y_preds(self, test_idx, train_idx, h):
        y_preds = []
        for i in range(len(test_idx)):
            total_weight = self.find_total_weight(test_idx[i], train_idx, h)
            y_pred = 0
            for j in range(len(train_idx)):
                y_pred += self.calc_kernel(test_idx[i],
                    train_idx[j],
                    h) * self.y_raw[train_idx[j]] / total_weight
            y_preds.append(y_pred)
        return y_preds

    def get_mse(self, y_preds, test_idx):
        n_test_points = len(test_idx)
        mse_unscaled = 0
        for i in range(n_test_points):
            mse_unscaled += (y_preds[i] - self.y_raw[test_idx[i]]) ** 2
        final_mse = mse_unscaled / n_test_points
        return final_mse

    def train(self):
        self.split()
        optimal_fold = []
        for idx in range(len(self.folds_idx)):
            local_fold = []
            test_idx = self.folds_idx[idx]
            train_idx_unflattened = [self.folds_idx[i] for i in range(len(self.folds_idx)) if i != idx]
            train_idx = reduce(lambda a, b: a + b, train_idx_unflattened)
            for h in self.bandwidths:
                y_preds = self.get_y_preds(test_idx, train_idx, h)
                mse = self.get_mse(y_preds, test_idx)
                local_fold.append((h, mse))
            local_optimal = self.find_best_mse(local_fold)
            optimal_fold.append(local_optimal)

        # After finding Optimal h, Train Whole Dataset
        self.optimal_h = self.find_best_mse(optimal_fold)[0]

    def predict(self):
        for i in range(len(self.x_raw)):
            # TODO: Make more efficient
            x_train = [j for j in range(len(self.x_raw)) if j != i]
            final_y_pred = self.get_y_preds([i], x_train, self.optimal_h)[0]
            self.final_y_preds.append(final_y_pred)

        return self.final_y_preds
