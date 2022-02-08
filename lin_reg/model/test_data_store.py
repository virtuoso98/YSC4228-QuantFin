from model.data_store import DataStore
import pytest
from random import random, randint, sample

def test_split():
    for _ in range(100):
        n_data = randint(2, 1000)
        n_folds = randint(2, n_data)
        # type of data should not affect
        test_x = [random() for _ in range(n_data)]
        test_y = [random() for _ in range(n_data)]
        raw_data = DataStore(test_x, test_y, n_folds)
        raw_data.split()
        folds_idx = raw_data.folds_idx
        assert len(folds_idx) == n_folds
        for fold in folds_idx:
            assert len(fold) - len(test_x) // n_folds >= 0
            assert len(fold) - len(test_x) // n_folds <= 1

def test_data_store_exception_unequal_length():
    # Test: x_raw, y_raw unequal length
    for _ in range(100):
        rand_index = sample(range(2, 1000), 2)
        n_folds = randint(2, min(rand_index))
        test_x = [random() for _ in range(rand_index[0])]
        test_y = [random() for _ in range(rand_index[1])]

        with pytest.raises(ValueError) as excinfo:
            _ = DataStore(test_x, test_y, n_folds)
            assert "Unequal X and Y Data Points" in excinfo.value

def test_data_store_exception_excessive_folds():
    #Test: number of folds exceed number of data points
    for _ in range(100):
        n_data = randint(2, 1000)
        n_folds = randint(n_data + 1, n_data + 1000)
        test_x = [random() for _ in range(n_data)]
        test_y = [random() for _ in range(n_data)]

        with pytest.raises(ValueError) as excinfo:
            raw_data = DataStore(test_x, test_y, n_folds)
            assert "Number of Folds exceed Number of Data Points" in excinfo.value

def test_data_store_exception_insufficient_folds():
    #Test: need at least 2 folds for validation
    for _ in range(100):
        n_data = randint(2, 1000)
        n_folds = randint(0, 1)
        test_x = [random() for _ in range(n_data)]
        test_y = [random() for _ in range(n_data)]

        with pytest.raises(ValueError) as excinfo:
            raw_data = DataStore(test_x, test_y, n_folds)
            assert "Need at least 2 folds for validation." in excinfo.value