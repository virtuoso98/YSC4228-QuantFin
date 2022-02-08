from functools import reduce
import math
from typing import Optional
from model.data_store import DataStore

class GaussianKernel(DataStore):
    """Kernel Class that Inherits from Datastore.

    Contains utility functions that help find the optimal
    h from a given train-test split and predicts y using
    the Gaussian Kernel

    Attributes:
        bandwidths: list of candidate h, one of which is optimal
        optimal_h: Globally optimal h obtained after training on K folds
        x_train: list of x values used as the training set
        y_train: list of y values used as the training set
        x_eval: list of x values to be evaluated at by training data
        y_eval: list of y values to be predicted by training data
    """

    def __init__(self, x_raw = None, y_raw = None, num_folds = 10):
        super().__init__(x_raw, y_raw, num_folds)
        # Attributes to find h
        self.bandwidths = [(i + 1) * 0.1 for i in range(20)]
        self.optimal_h = None
        # Train - Test Split
        self.x_train = []
        # x where values will be evaluated at
        self.x_eval = []
        # To find the MSE and find optimal h
        self.y_train = []
        self.y_eval = []


    def _calc_kernel(self, x1: float, x2: float, h: float) -> float:
        """Calculates the Gaussian Kernel based on given formula

        The given formula is e ** (- (x1 - x2) ** 2 / h). This
        is the basis of the Gaussian Kernel.

        Args:
            x1: first x value
            x2: second x value
            h: bandwidth used for calculation

        Returns:
            Calculated kernel, in float
        """
        x_delta = (x1 - x2) ** 2
        return math.exp(- x_delta / h)

    def _find_total_weight(self, x_ev: float, h: float) -> float:
        """Finds sum of kernels of x to be predicted against all training x

        This function uses what was defined in calc_kernel to find
        total weight, thereby minimizing code repetition

        Args:
            x_ev: input to predict y at x_ev
            h: bandwidth used to find total weight

        Returns:
            Sum of the total kernel of a x against training x
        """
        total_weight = 0
        for x_tr in self.x_train:
            total_weight += self._calc_kernel(x_ev, x_tr, h)
        return total_weight


    def _get_y_pred(self, h: float) -> list[float]:
        """Gets predicted y iteratively, using kernel formula

        Args:
            h: bandwidth used to predict y

        Returns:
            list of float of predicted y values
        """
        y_preds = []
        for x_ev in self.x_eval:
            # find total weight of kernel
            total_weight = self._find_total_weight(x_ev, h)
            y_pred = 0
            # calculate y_pred based on weight
            for i, x_tr in enumerate(self.x_train):
                y_pred += self._calc_kernel(x_ev,
                    x_tr, h) * self.y_train[i] / total_weight
            y_preds.append(y_pred)
        return y_preds

    def _get_mse(self, y_preds: list[float])-> float:
        """Method used to find MSE between predicted y and actual y

        Args:
            y_preds:
        Returns:
            Mean-squared error of the y
        """
        n_test = len(self.y_eval)
        mse_unscaled = 0
        for i in range(n_test):
            mse_unscaled += (y_preds[i] - self.y_eval[i]) ** 2
        mse = mse_unscaled / n_test
        return mse

    def _find_best_mse(self, y_pred_and_mse):
        """Finds optimal h based on MSE

        Args:
            y_pred_and_mse: a list containing tuples of (h, mse)

        Returns:
            A tuple containing the lowest mse in the form (h, mse)
        """
        return min(y_pred_and_mse, key = lambda tup: tup[1])

    def train(self):
        """Overall function used to find the optimal h.

        The steps used to achieve the optimal h are as follows:
        1. Split data to K folds for validation
        2. For Each fold, do the following:
        - allocate training and evaluation data
        - use kernel regression to get predicted y
        - find mean squared error
        - collect optimal h within the fold with minimum MSE
        3. Find globally optimal h across all folds
        4. Store this value as self.optimal_h
        """
        self.split()
        n_folds = len(self.folds_idx)
        optimal_h_for_fold = []
        for i in range(n_folds):
            local_fold = []
            # Get appropriate train test split
            test_idx = self.folds_idx[i]
            train_tmp = [self.folds_idx[j] for j in range(n_folds) if i != j]
            train_idx = reduce(lambda a, b: a + b, train_tmp)
            # Allocate actual train-test split
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

    def predict(self,
        x_to_predict: Optional[float]
        ) -> Optional[float]:
        """Overall Function to predict y values.

        x_to_predict flag determines whether predictions should be
        done on xout or xin instead.

        Args:
            x_to_predict: None or contains a arr of x to predict

        Returns:
            A float array of corresponding predicted y values
        """
        # if there is xout, predict xout using xin, yin
        if x_to_predict is not None:
            self.x_train = self.x_raw
            self.y_train = self.y_raw
            self.x_eval = x_to_predict
            return self._get_y_pred(self.optimal_h)

        n_pts = len(self.x_raw)
        output = []
        for i in range(n_pts):
            self.x_eval = [self.x_raw[i]]
            self.x_train = [self.x_raw[j] for j in range(n_pts) if j != i]
            self.y_train = [self.y_raw[j] for j in range(n_pts) if j != i]
            # y_pred is now just a singleton list
            y_pred = self._get_y_pred(self.optimal_h)
            output.append(y_pred[0])
        return output

    def train_and_predict(self, x_to_predict):
        """Overall function that runs kernel. See train
        or predict for more information.
        """
        self.train()
        return self.predict(x_to_predict)
