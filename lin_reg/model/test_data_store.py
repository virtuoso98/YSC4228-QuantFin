from data_store import DataStore
import math, pytest
from random import random, randint

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

def test_data_store_exception():
    # Test 1: x_raw, y_raw unequal length
    test_x = [i + 2 for i in range(7)]
    test_y = [i - 1 for i in range(10)]
    n_folds = 3

    with pytest.raises(ValueError) as excinfo:
        _ = DataStore(test_x, test_y, n_folds)
        assert "Unequal X and Y Data Points" in excinfo.value

    #Test 2: number of folds exceed number of data points
    test_x = [i - 1 for i in range(10)]
    test_y = [i + 1 for i in range(10)]
    n_folds = 13

    with pytest.raises(ValueError) as excinfo:
        raw_data = DataStore(test_x, test_y, n_folds)
        assert "Number of Folds exceed Number of Data Points" in excinfo.value

    #Test 3: need at least 2 folds for validation
    test_x = [i + 2 for i in range(10)]
    test_y = [i - 1 for i in range(10)]
    n_folds = 1

    with pytest.raises(ValueError) as excinfo:
        raw_data = DataStore(test_x, test_y, n_folds)
        assert "Need at least 2 folds for validation." in excinfo.value