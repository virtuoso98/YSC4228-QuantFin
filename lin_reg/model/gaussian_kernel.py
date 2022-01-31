from model.data_store import DataStore
import math

class GaussianKernel(DataStore):

    def __init__(self, x_raw, y_raw, num_folds) -> None:
        super().__init__(x_raw, y_raw, num_folds)
        self.mse = []
        # Finding the optimal bandwidth
        self.bandwidths = [0.1 * (i + 1) for i in range(20)]

    def calc_kernel(self, i, j, h) -> float:
        x_delta = (self.x_raw[i] - self.x_raw[j]) ** 2
        return math.exp(- x_delta / h)

    def train(self):
        self.split()
           