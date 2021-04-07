import sys
import io
from contextlib import contextmanager
from unittest import TestCase
from convect.command_line import main


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestConsole(TestCase):
    def test_hello(self):
        with captured_output() as (out, err):
            main()
        output = out.getvalue().strip()
        self.assertEqual(
            output,
            "Welcome to Convect! Head over to https://app.convect.ml to get started with deploying models."
        )
