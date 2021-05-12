import io
import sys
import __main__ as _main_module
from contextlib import contextmanager

import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.linear_model import LinearRegression

reg = LinearRegression().fit([[0, 0], [0, 1], [2, 2]], [0, 1, 2])


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def setup_newsgroups_func():
    setattr(_main_module, 'newsgroups', fetch_20newsgroups(
        shuffle=True,
        random_state=1,
        remove=('headers', 'footers', 'quotes')
    ))


def teardown_newsgroups_func():
    delattr(_main_module, 'newsgroups')


class MockModule:
    def __init__(self, attr_name, attr_val):
        setattr(self, attr_name, attr_val)


def setup_ipython_module_func():
    setattr(
        _main_module, "ipython_module", MockModule(
            "__module__", "IPython.core.abcd"
        )
    )


def teardown_ipython_module_func():
    delattr(_main_module, 'ipython_module')


def raise_(ex):  # Helper for raising exceptions in a lambda function
    raise ex
