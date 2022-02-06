import numpy as np

class DataStore:
    def __init__(self, x_raw, y_raw, num_folds = 10) -> None:
        # Check if number of x and y data points tally
        if len(x_raw) != len(y_raw):
            raise ValueError("Unequal X and Y Data Points")
        # Check if number of folds do not tally
        if num_folds > len(x_raw):
            raise ValueError("Number of Folds exceed Number of Data Points")

        if num_folds <= 1:
            raise ValueError("Need at least 2 folds for validation.")

        self.x_raw = x_raw
        self.y_raw = y_raw
        self.num_folds = num_folds
        # To be defined upon execution of split method
        self.folds_idx = None

    def split(self, seed = 100) -> None:
        np.random.seed(seed)
        idx_arr = list(range(len(self.x_raw)))
        np.random.shuffle(idx_arr)
        np_split_array = np.array_split(idx_arr, self.num_folds)
        self.folds_idx = [list(fold) for fold in np_split_array]

    @classmethod
    def train(cls):
        pass

    @classmethod
    def predict(cls):
        pass
