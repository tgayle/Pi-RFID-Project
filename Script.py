from enum import Enum

TYPES = ["PRINT", "PY_SCRIPT", "BASH_SCRIPT"]


class Script:
    def __init__(self, type, script):

        if (isinstance(type, Type)):
            self.__type = type
        else:
            raise RuntimeError("Type for class wasn't correct " + type)

        self.__script = script

    def type(self):
        return self.__type
    def script(self):
        return self.__script


class Type(Enum):

    '''
    PRINT - Return a string after card is scanned
    PY_SCRIPT - Launch a written python script from database/py/
    BASH_SCRIPT - Launch a bash script from database/bash/
    '''
    def __init__(self, script_type):
        if script_type in TYPES:
            self.__script_type = script_type
        else:
            raise RuntimeError("Tried to create script type %s but this isn't valid." % script_type)

    def script_type(self):
        return self.__script_type
