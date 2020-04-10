"""
hvmParser.py -- Parser class for Hack VM translator
"""

from hvmCommands import *


class Parser(object):
    def __init__(self, sourceName, comments=None):
        """
        Open 'sourceFile' and gets ready to parse it.
        """
        self.file = open(sourceName, 'r')
        self.lineNumber = 0
        self.line = ''
        self.rawline = ''
        self.comments = comments

    def Advance(self):
        """
        Reads the next command from the input and makes it the current
        command.
        Returns True if a command was found, False at end of file.
        """
        while True:
            if self.file:
                self.rawline = self.file.readline()
                if len(self.rawline) == 0:
                    return False
                self.rawline = self.rawline.replace('\n', '')
                self.line = self.rawline
                i = self.line.find('//')
                if i != -1:
                    if self.comments:
                        self.comments.Write('    ' + self.line[i:])
                    self.line = self.line[:i]
                self.line = self.line.replace('\t', ' ').strip()
                if len(self.line) == 0:
                    continue
                self._Parse(self.line)
                return True
            else:
                return False

    def CommandType(self):
        """
        Returns the type of the current command:
            C_ARITHMETIC = 1
            C_PUSH = 2
            C_POP = 3
            C_LABEL = 4
            C_GOTO = 5
            C_IF = 6
            C_FUNCTION = 7
            C_RETURN = 8
            C_CALL = 9
        """
        return self.commandType

    def Arg1(self):
        """
        Returns the command's first argument.
        """
        return self.arg1

    def Arg2(self):
        """
        Returns the command's second argument.
        """
        return self.arg2

    """
    The function to be implemented.
	For Project 6 the function should parse PUSH/POP and the arithmetic commands.
	Parses the current comment. Assumes that there is a single whitespace between the command and between each argument (there can be up to 2 arguments).
	Fills in 'commandType', 'arg1' and 'arg2'.
    Some examples:
---------------------------------------------------------------------
|        currentLine	-> desired contents							|
---------------------------------------------------------------------
| "push constant 2"		-> arg1="constant", arg2=2		|
| "call yourfunction 3" -> arg1="yourfunction", arg2=3	|
| "and"					-> arg1="and", arg2=0				|
| "label xyz"			-> arg1="xyz"							|
---------------------------------------------------------------------
    """

    def _Parse(self, currentLine):
        # command [arg1 [arg2]]
        currentLine = currentLine.split(" ")  # self.comments.split(" ")

        n = len(currentLine)
        # this should store the type of the command
        try:
            self.commandType = eval("C_" + currentLine[0].upper())
        except:
            self.commandType = C_ARITHMETIC
            self.arg1 = currentLine[0]
            return

        # this should store the first argument of the command (if there is a first argument)
        self.arg1 = None
        if not self.commandType == C_ARITHMETIC and not self.commandType == "C_RETURN":
            self.arg1 = currentLine[1]

        # this should store the second argument of the command (if there is a second argument)
        self.arg2 = None
        condition = [C_PUSH, C_POP, C_FUNCTION, C_CALL]
        if n > 1 and self.commandType in condition:
            self.arg2 = currentLine[2]
