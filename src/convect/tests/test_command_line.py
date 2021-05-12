import sys
from unittest.mock import patch

from nose.tools import assert_equal

from convect.tests import captured_output
from convect.command_line import main

def test_ready():
    with patch.object(sys, 'argv', ['blah/convect', 'ready']):
        with captured_output() as (out, err):
            main()
    output = out.getvalue().strip()
    assert_equal(
        output,
        "Welcome to Convect!\n\nHead to https://app.convect.ml to start deploying models."
    )


def test_invalid():
    with patch.object(sys, 'argv', ['blah/convect', 'asdf']):
        with captured_output() as (out, err):
            main()
    output = out.getvalue().strip()
    assert_equal(
        output,
        "Invalid usage of convect. Try:\n\nconvect ready"
    )
