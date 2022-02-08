from model.gaussian_kernel import GaussianKernel
from random import uniform, randint, random
import pytest, math

def test_calc_kernel():
    # Init kernel with dummy variables so exception
    # does not occur. However, calc_kernel is static,
    # so dummy values don't matter
    dummy_data = [0, 0]
    dummy_folds = 2
    raw_data = GaussianKernel(dummy_data, dummy_data, dummy_folds)

    for _ in range(100):
        test_x1 = uniform(-1000, 1000)
        test_x2 = uniform(-1000, 1000)
        test_h = uniform(0.1, 3)
        
        # Actual Value
        actual_kernel = raw_data._calc_kernel(test_x1, test_x2, test_h)

        # Expected value
        x_delta = (test_x1 - test_x2) ** 2
        expected_kernel = math.exp(- x_delta / test_h)

        # Testing that they are equivalent, modulo floating pt error
        assert abs(expected_kernel - actual_kernel) < 10 ** -6

def test_find_total_weight():
    # Populate test x to evaluate
    test_x_ev = uniform(-10, 10)
    test_h = uniform(0.1, 3)
    # Populate test data
    n_data = randint(2, 1000)
    n_folds = randint(2, n_data)
    test_x_train = [uniform(-10, 10) for _ in range(n_data)]
    # Y dummy as it's not important to the test
    dummy_y = [0 for _ in range(n_data)]
    raw_data = GaussianKernel(test_x_train, dummy_y, n_folds)
    # Can only test find_total_weight by populating x_train directly
    raw_data.x_train = test_x_train

    #Actual value
    actual_weight = raw_data._find_total_weight(test_x_ev, test_h)

    #Expected value
    expected_weight = 0
    for x_tr in raw_data.x_train:
        x_delta = (test_x_ev - x_tr) ** 2
        expected_weight += math.exp(- x_delta / test_h)

    # Testing that they are equivalent, modulo floating pt error
    assert abs(expected_weight - actual_weight) < 10 ** -6

def test_get_y_pred():
    # Populate test x to evaluate
    test_x_ev = uniform(-10, 10)
    test_h = uniform(0.1, 3)
    # Populate test data
    n_data = randint(2, 1000)
    n_folds = randint(2, n_data)
    test_x_train = [uniform(-10, 10) for _ in range(n_data)]
    # Y dummy as it's not important to the test
    dummy_y = [0 for _ in range(n_data)]
    raw_data = GaussianKernel(test_x_train, dummy_y, n_folds)
    # Can only test find_total_weight by populating x_train directly
    raw_data.x_train = test_x_train

    

    