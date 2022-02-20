import numpy as np

class DataStore:
    """Class that handles raw data storing and train-test split.

    This is a general class that will be inherited by the Gaussian
    Kernel class.

    Attributes:
        x_raw: list containing x input data in float.
        y_raw: list containing y input data in float.
        num_folds: Number of folds used to split data for validation.
        folds_idx: list containing the fold splits by indexes.
    """

    def __init__(self,
        x_raw: "list[float]",
        y_raw: "list[float]",
        num_folds: int = 10) -> None:
        # Check if number of x and y data points tally
        if len(x_raw) != len(y_raw):
            raise ValueError("Unequal X and Y Data Points")
        # Check if number of folds do not tally
        if num_folds > len(x_raw):
            raise ValueError("Number of Folds exceed Number of Data Points")
        # Check if number of folds is insufficient
        if num_folds <= 1:
            raise ValueError("Need at least 2 folds for validation.")

        self.x_raw = x_raw
        self.y_raw = y_raw
        self.num_folds = num_folds
        # To be defined upon execution of split method.
        # Example of folds_idx: [[0, ], [2, 3], [1, 4]]
        self.folds_idx = None

    def split(self, seed: int = 100) -> None:
        """Performs K folds splitting using numpy.

        Given N data points, this function creates an array of indexes,
        randomly shuffles them and splits them into subarrays, updating
        the folds_idx attribute.

        Args:
            seed (int): Initializer for PRNG so results are replicable
        """
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
