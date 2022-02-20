import sys
import pytest
from local_linear import execute

def test_xin_file_not_found():
    """Test with a xin file name that does not exist"""
    with pytest.raises(OSError):
        xin_not_exist = 'xin_not_exist'
        argv_head = [sys.argv[0]]
        new_args = ["--x", xin_not_exist,
            "--y", "yin",
            "--output", "output",
            "--num_folds", "10",
            "--plot", "True",
            "--xout", "xout"
        ]
        sys.argv = argv_head + new_args
        execute()


def test_yin_file_not_found():
    """Test with a yin file name that does not exist"""
    with pytest.raises(OSError):
        yin_not_exist = "yin_not_exist"
        argv_head = [sys.argv[0]]
        new_args = ["--x", "xin",
            "--y", yin_not_exist,
            "--output", "output",
            "--num_folds", "10",
            "--plot", "True",
            "--xout", "xout"
        ]
        sys.argv = argv_head + new_args
        execute()

def test_xout_file_not_found():
    """Test with a xout file name that does not exist"""
    with pytest.raises(OSError):
        xout_not_exist = "xout_not_exist"
        argv_head = [sys.argv[0]]
        new_args = ["--x", "xin",
            "--y", "yin",
            "--output", "output",
            "--num_folds", "10",
            "--plot", "True",
            "--xout", xout_not_exist
        ]
        sys.argv = argv_head + new_args
        execute()

def test_bad_num_fold_param():
    """Non numeric fold param causes system exit"""
    with pytest.raises(SystemExit):
        bad_num_fold = "abc123"
        argv_head = [sys.argv[0]]
        new_args = ["--x", "xin",
            "--y", "yin",
            "--output", "output",
            "--num_folds", bad_num_fold,
            "--plot", "True",
            "--xout", "xout"
        ]
        sys.argv = argv_head + new_args
        execute()
