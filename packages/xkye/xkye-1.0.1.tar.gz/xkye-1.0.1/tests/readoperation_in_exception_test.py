"""
Test to check the read-in operation exception
"""

import os

import pytest

from xkye import IO as io


# To test if the span for the clutch is already declared
def test_read_file_in_exception_1():

    """ test_read_file_in_exception_1 """
    xky_file = "in/read_in_exception_1.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if the key is already declared for the clutch
def test_read_file_in_exception_2():

    """ test_read_file_in_exception_2 """
    xky_file = "in/read_in_exception_2.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if clutchset span is greater than the declared span limit
def test_read_file_in_exception_3():

    """ test_read_file_in_exception_3  """
    xky_file = "in/read_in_exception_3.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if clutchset is not declared with the span limit
def test_read_file_in_exception_4():

    """ test_read_file_in_exception_4  """
    xky_file = "in/read_in_exception_4.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if subclutch is not defined before this call
def test_read_file_in_exception_5():

    """ test_read_file_in_exception_5  """
    xky_file = "in/read_in_exception_5.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if the defined subclutch span is exceeding declared span limit
def test_read_file_in_exception_6():

    """ test_read_file_in_exception_6 """
    xky_file = "in/read_in_exception_6.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None
