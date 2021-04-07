import sys
import io
from contextlib import contextmanager
from unittest import TestCase
from convect.command_line import main
from unittest.mock import patch


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
        with patch.object(sys, 'argv', ['blah/convect', 'hello']):
            with captured_output() as (out, err):
                main()
        output = out.getvalue().strip()
        self.assertEqual(
            output,
            "Welcome to Convect!\n\nHead to https://app.convect.ml to start deploying models."
        )

    def test_invalid(self):
        with patch.object(sys, 'argv', ['blah/convect', 'asdf']):
            with captured_output() as (out, err):
                main()
        output = out.getvalue().strip()
        self.assertEqual(
            output,
            "Invalid usage of convect. Try:\n\nconvect hello"
        )
