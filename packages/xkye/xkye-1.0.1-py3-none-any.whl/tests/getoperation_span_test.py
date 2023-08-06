"""
To test the span method
"""

import os

import pytest

from xkye import IO as io


# To test if the clutch is present in the given file
def test_get_span_method_success():

    """ test_get_span_method_success """
    xky_file = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    xkye = io(xky_file)
    xkye.read()

    valued = xkye.getSpan("shard")

    assert int(valued) == 4


# To test if the clutch is not present in the given file
def test_get_span_method_failure():

    """ test_get_span_method_failure """
    xky_file = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    xkye = io(xky_file)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.getSpan("shard not in clutch")
        assert valued is None
