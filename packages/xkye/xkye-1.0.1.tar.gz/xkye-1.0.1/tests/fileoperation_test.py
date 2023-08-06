"""
Tests for file related operation
"""

import os

import pytest

from xkye import IO as io


# To test the missing file
def test_missing_input_file():

    """ To test the missing input file  """
    xky_file = "../test/test.xky"
    with pytest.raises(Exception):
        mxkye = io(xky_file)
        assert mxkye.read() is None


# To test the read operation
def test_input_file_success():

    """ to test the correct input file """
    xky_file = "in/test.xky"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    xkye = io(xky_file)
    dictionary = xkye.read()
    assert dictionary is True
