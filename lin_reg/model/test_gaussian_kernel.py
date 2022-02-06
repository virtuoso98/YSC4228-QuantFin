from gaussian_kernel import GaussianKernel
import pytest

def test_split():

    test_x = [i + 2 for i in range(10)]
    test_y = [i - 1 for i in range(10)]
    n_folds = 3
    raw_data = GaussianKernel(test_x, test_y, n_folds)
    raw_data.split()

    folds_idx = raw_data.folds_idx
    assert(len(folds_idx) == n_folds)
    for fold in folds_idx:
        assert(len(fold) - len(test_x) // n_folds >= 0)
        assert(len(fold) - len(test_x) // n_folds <= 1)