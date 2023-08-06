"""
To test the read-out exception
"""

import os

import pytest

from xkye import IO as io


# To test if clutch span and clutch is not defined & the entity is not in the defined clutch
def test_read_file_out_exception_1():

    """ test_read_file_out_exception_1 """
    xky_file = "in/read_out_exception_1.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if clutch span is not defined & the entity is not in the defined clutch
def test_read_file_out_exception_2():

    """ test_read_file_out_exception_2 """
    xky_file = "in/read_out_exception_2.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if clutch span is not defined & the defined clutch is none
def test_read_file_out_exception_3():

    """ test_read_file_out_exception_3  """
    xky_file = "in/read_out_exception_3.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if clutch(shard3) is none and entity not in default clutch(shard)
def test_read_file_out_exception_4():

    """ test_read_file_out_exception_4  """
    xky_file = "in/read_out_exception_4.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test the scenario when the resquested clutch and its default clutch is none
def test_read_file_out_exception_5():

    """ test_read_file_out_exception_5  """
    xky_file = "in/read_out_exception_5.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None


# To test if entity not in both clutch(shard3) and default clutch(shard)
def test_read_file_out_exception_6():

    """ test_read_file_out_exception_6  """
    xky_file = "in/read_out_exception_6.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xky_file = dir_path + "/" + xky_file

    with pytest.raises(Exception):
        xkye = io(xky_file)
        dictionary = xkye.read()
        assert dictionary is None
