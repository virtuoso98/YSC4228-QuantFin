from model.data_store import DataStore
from functools import reduce
import math

class GaussianKernel(DataStore):

    def __init__(self, x_raw = None, y_raw = None, num_folds = 10) -> None:
        super().__init__(x_raw, y_raw, num_folds)
        # Evaluation Variables
        self.mse = []
        self.bandwidths = [(i + 1) * 0.1 for i in range(20)]
        self.optimal_h = None
        # Train - Test Split
        self.x_train = []
        # To find the MSE and find optimal h
        self.y_train = []
        self.y_eval = []
        # x where values will be evaluated at
        self.x_eval = []


    def _calc_kernel(self, x1, x2, h) -> float:
        x_delta = (x1 - x2) ** 2
        return math.exp(- x_delta / h)

    def _find_total_weight(self, x_ev, h) -> float:
        total_weight = 0
        for x_tr in self.x_train:
            total_weight += self._calc_kernel(x_ev, x_tr, h)
        return total_weight


    def _get_y_pred(self, h):
        y_preds = []
        for x_ev in self.x_eval:
            total_weight = self._find_total_weight(x_ev, h)
            y_pred = 0
            for i, x_tr in enumerate(self.x_train):
                y_pred += self._calc_kernel(x_ev, x_tr, h) * self.y_train[i] / total_weight
            y_preds.append(y_pred)
        return y_preds

    def _get_mse(self, y_preds):
        n_test = len(self.y_eval)
        mse_unscaled = 0
        for i in range(n_test):
            mse_unscaled += (y_preds[i] - self.y_eval[i]) ** 2
        mse = mse_unscaled / n_test
        return mse

    def _find_best_mse(self, y_pred_and_mse):
        """Finds minimum mean squared error
        """
        return min(y_pred_and_mse, key = lambda tup: tup[1])

    def train(self):
        self.split()
        n_folds = len(self.folds_idx)
        optimal_h_for_fold = []
        for i in range(n_folds):
            local_fold = []
            # Get appropriate train test split
            test_idx = self.folds_idx[i]
            train_idx_unflattened = [self.folds_idx[j] for j in range(n_folds) if i != j]
            train_idx = reduce(lambda a, b: a + b, train_idx_unflattened)
            # Allocate to appropriate classes
            self.x_eval = [self.x_raw[k] for k in test_idx]
            self.y_eval = [self.y_raw[k] for k in test_idx]
            self.x_train = [self.x_raw[k] for k in train_idx]
            self.y_train = [self.y_raw[k] for k in train_idx]
            # begin evaluation of h for different folds
            for h in self.bandwidths:
                y_pred_fold = self._get_y_pred(h)
                mse = self._get_mse(y_pred_fold)
                local_fold.append((h, mse))

            local_optimal = self._find_best_mse(local_fold)
            optimal_h_for_fold.append(local_optimal)
        # After finding Optimal h, Train Whole Dataset
        self.optimal_h = self._find_best_mse(optimal_h_for_fold)[0]

    def predict(self, x_to_predict):
        if x_to_predict is not None:
            self.x_train = self.x_raw
            self.y_train = self.y_raw
            self.x_eval = x_to_predict
            return self._get_y_pred(self.optimal_h)
        else:
            n_points = len(self.x_raw)
            output = []
            for i in range(n_points):
                self.x_eval = [self.x_raw[i]]
                self.x_train = [self.x_raw[j] for j in range(n_points) if j != i]
                self.y_train = [self.y_raw[j] for j in range(n_points) if j != i]
                # y_pred is now just a singleton list 
                y_pred = self._get_y_pred(self.optimal_h)
                output.append(y_pred[0])
            return output
