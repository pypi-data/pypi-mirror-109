"""
XkyeModel.py: To perfrom Xkye language operations
"""

import os


from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from multipledispatch import dispatch


from .libs import XkyeLexer, XkyeParser, XkyeExtendedListener


class IO:

    """Class to execute input output related methods"""

    # To initiate the read write operation
    def __init__(self, filename):

        self.filename = filename
        self.out_dict = {}
        self.out_span = []

    # To convert the input file into the outdictionary
    def read(self):

        """To convert the input file into the outdictionary"""
        if not os.path.isfile(self.filename):
            raise Exception(
                'File "'
                + self.filename
                + '" is missing, kindly check the path or provide the absolute path'
            )

        # Else perfrom xky file reading task
        input_file = FileStream(self.filename)
        lexer = XkyeLexer(input_file)
        stream = CommonTokenStream(lexer)
        parser = XkyeParser(stream)
        tree = parser.globe()
        listendx = XkyeExtendedListener(self.out_dict, self.out_span)

        walker = ParseTreeWalker()
        walker.walk(listendx, tree)

        return True

    # To read the values with single input
    @dispatch(str)
    def get(self, entity):

        """To read the values with single input"""
        dict_list = list(self.out_dict["global"].keys())

        if entity not in dict_list:
            raise Exception(
                'Requested entity "'
                + entity
                + '" not declared. kindly check your input .xky file'
            )

        result = self.out_dict["global"][entity]
        return result

    # To read the values with double input
    @dispatch(str, str)
    def get(self, entity, substr):  # pylint: disable-msg=E0102

        """To read the values with double input"""
        dict_list = list(self.out_dict.keys())

        if substr not in dict_list:
            raise Exception(
                'Requested clutch "'
                + substr
                + '" is not declared. kindly check your input .xky file'
            )

        if entity not in list(self.out_dict[substr].keys()):
            raise Exception(
                'Requested entity "'
                + entity
                + '" not declared. kindly check your input .xky file'
            )

        result = self.out_dict[substr][entity]
        return result

    # To read the values with triple input
    @dispatch(str, str, int)
    def get(self, entity, substr, subnumber):  # pylint: disable-msg=E0102

        """To read the values with triple input"""
        subnumber = str(subnumber)
        substrnew = substr + subnumber

        dict_list = list(self.out_dict.keys())

        if substrnew not in dict_list:
            if substr in dict_list:
                if entity in list(self.out_dict[substr].keys()):
                    result = self.out_dict[substr][entity]
                    return result

                raise Exception(
                    'Requested entity "'
                    + entity
                    + '" not declared. kindly check your input .xky file'
                )

            raise Exception(
                'Requested clutch "'
                + substr
                + '" is not declared. kindly check your input .xky file'
            )

        if entity not in list(self.out_dict[substrnew].keys()):
            if entity in list(self.out_dict[substr].keys()):
                result = self.out_dict[substr][entity]
                return result

            raise Exception(
                'Requested entity "'
                + entity
                + '" not declared. kindly check your input .xky file'
            )

        result = self.out_dict[substrnew][entity]
        return result

    # To get the declared span for the specified clutch
    @dispatch(str)
    def getSpan(self, clutch):  # pylint: disable-msg=C0103

        """To get the span value of the cluster"""
        clutch_list = []
        span_list = []

        for clutchpair in self.out_span:
            clutch_list.append(clutchpair[0])
            span_list.append(clutchpair[1])

        if clutch not in clutch_list:
            raise Exception(
                'Requested clutch "'
                + clutch
                + '" not declared. kindly check your input .xky file'
            )

        index = clutch_list.index(clutch)
        span_value = span_list[index]

        return span_value
