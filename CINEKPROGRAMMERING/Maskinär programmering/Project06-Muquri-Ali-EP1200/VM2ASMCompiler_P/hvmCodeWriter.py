"""
hvmCodeWriter.py -- Code Writer class for Hack VM translator
"""

import os
from hvmCommands import *

debug = False


class CodeWriter(object):

    def __init__(self, outputName):
        """
        Open 'outputName' and gets ready to write it.
        """
        self.file = open(outputName, 'w')
        self.SetFileName(outputName)

        self.labelNumber = 0
        self.returnLabel = None
        self.callLabel = None
        self.cmpLabels = {}
        self.needHalt = True

    def Debug(self, value):
        """
        Set debug mode.
        Debug mode writes useful comments in the output stream.
        """
        global debug
        debug = value

    def Close(self):
        """
        Write a jmp $ and close the output file.
        """
        if self.needHalt:
            if debug:
                self.file.write('    // <halt>\n')
            label = self._UniqueLabel()
            self._WriteCode('@%s, (%s), 0;JMP' % (label, label))
        self.file.close()

    def SetFileName(self, fileName):
        """
        Sets the current file name to 'fileName'.
        Restarts the local label counter.

        Strips the path and extension.  The resulting name must be a
        legal Hack Assembler identifier.
        """
        if (debug):
            self.file.write('    // File: %s\n' % (fileName))
        self.fileName = os.path.basename(fileName)
        self.fileName = os.path.splitext(self.fileName)[0]
        self.functionName = None

    def Write(self, line):
        """
        Raw write for debug comments.
        """
        self.file.write(line + '\n')

    def _UniqueLabel(self):
        """
        Make a globally unique label.
        The label will be _sn where sn is an incrementing number.
        """
        self.labelNumber += 1
        return '_' + str(self.labelNumber)

    def _LocalLabel(self, name):
        """
        Make a function/module unique name for the label.
        If no function has been entered, the name will be
        FileName$$name. Otherwise it will be FunctionName$name.
        """
        if self.functionName != None:
            return self.functionName + '$' + name
        else:
            return self.fileName + '$$' + name

    def _StaticLabel(self, index):
        """
        Make a name for static variable 'index'.
        The name will be FileName.index
        """
        return self.fileName + '.' + str(index)

    def _WriteCode(self, code):
        """
        Write the comma separated commands in 'code'.
        """
        code = code.replace(',', '\n').replace(' ', '')
        self.file.write(code + '\n')

    """"
    The functions to be implemented are found beyond this point
    """

    """
    Parameters:

    Result:
    For push: Pushes the content of segment[index] onto the stack. It is a good idea to move the value to be pushed into a register first, then push the content of the register to the stack.
    For pop: Pops the top of the stack into segment[index]. You may need to use a general purpose register (R13-R15) to store some temporary results.
    Returns:
    Nothing.
    Hint: Recall that there are 8 memory segments in the VM model, but only 5 of these exist in the assembly definition. Also, not all 8 VM segments allow to perform both pop and push on them. Chapter 7.3 of the book explains memory segment mapping.
    Hint: Use pen and paper first. Figure out how to compute the address of segment[index] (except for constant). Then figure out how you move the value of segment[index] into a register (by preference D). Then figure out how to push a value from a register onto the stack.
    Hint: For pop, you already know how to compute the address of segment[index]. Store it in a temporary register (you can use R13 to R15 freely). Then read the value from the top of the stack, adjust the top of the stack, and then store the value at the location stored in the temporary register.
    """

    def WritePushPop(self, commandType, segment, index):
        sgmtType = eval("S_" + segment.upper())
        text = []
        appendage = []
        if not index == 'CALL':
            text.extend(("@" + str(index), "D=A"))

        if commandType == C_PUSH:

            if sgmtType == S_ARGUMENT:
                appendage = ["@ARG", "A=D+M"]

            elif sgmtType == S_LOCAL:
                appendage = ["@LCL", "A=D+M"]

            elif sgmtType == S_STATIC:
                appendage = ["@16", "A=D+A"]

            elif sgmtType == S_THIS:
                appendage = ["@THIS", "A=D+M"]

            elif sgmtType == S_THAT:
                appendage = ["@THAT", "A=D+M"]

            elif sgmtType == S_POINTER:
                appendage = ["@3", "A=D+A"]

            elif sgmtType == S_TEMP:
                appendage = ["@5", "A=D+A"]

            text.extend(appendage)

            if sgmtType == S_CONSTANT:
                text.extend(("@SP", "A=M", "M=D", "@SP", "M=M+1"))
            else:
                if index == 'CALL':
                    appendage = appendage[0]
                    text.append(appendage)
                else:
                    text.extend(appendage)
                text.extend(("D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"))

        elif commandType == C_POP:

            if sgmtType == S_ARGUMENT:
                appendage = ["@ARG", "D=D+M"]

            elif sgmtType == S_LOCAL:
                appendage = ["@LCL", "D=D+M"]

            elif sgmtType == S_STATIC:
                appendage = ["@16", "D=D+A"]

            elif sgmtType == S_THIS:
                appendage = ["@THIS", "D=D+M"]

            elif sgmtType == S_THAT:
                appendage = ["@THAT", "D=D+M"]

            elif sgmtType == S_POINTER:
                appendage = ["@3", "D=D+A"]

            elif sgmtType == S_TEMP:
                appendage = ["@5", "D=D+A"]

            text.extend(appendage)
            text.extend(("@13", "M=D", "@SP", "AM=M-1",
                         "D=M", "@13", "A=M", "M=D"))
        newline = '\n'
        code = newline.join(text)
        self._WriteCode(code)

        """
        Write Hack code for 'commandType' (C_PUSH or C_POP).
        'segment' (string) is the segment name.
        'index' (int) is the offset in the segment.
	To be implemented as part of Project 6

	    For push: Pushes the content of segment[index] onto the stack. It is a good idea to move the value to be pushed into a register first, then push the content of the register to the stack.
        For pop: Pops the top of the stack into segment[index]. You may need to use a general purpose register (R13-R15) to store some temporary results.
        Hint: Recall that there are 8 memory segments in the VM model, but only 5 of these exist in the assembly definition. Also, not all 8 VM segments allow to perform both pop and push on them. Chapter 7.3 of the book explains memory segment mapping.
        Hint: Use pen and paper first. Figure out how to compute the address of segment[index] (except for constant). Then figure out how you move the value of segment[index] into a register (by preference D). Then figure out how to push a value from a register onto the stack.
        Hint: For pop, you already know how to compute the address of segment[index]. Store it in a temporary register (you can use R13 to R15 freely). Then read the value from the top of the stack, adjust the top of the stack, and then store the value at the location stored in the temporary register.

        """

    def WriteArithmetic(self, command):
        """
        Write Hack code for stack arithmetic 'command' (str).
        To be implemented as part of Project 6

                Compiles the arithmetic VM command into the corresponding ASM code. Recall that the operands (one or two, depending on the command) are on the stack and the result of the operation should be placed on the stack.
        The unary and the logical and arithmetic binary operators are simple to compile.
         The three comparison operators (EQ, LT and GT) do not exist in the assembly language. The corresponding assembly commands are the conditional jumps JEQ, JLT and JGT. You need to implement the VM operations using these conditional jumps. You need two labels, one for the true condition and one for the false condition and you have to put the correct result on the stack.
        """
        text = []
        conditionCmp = [T_EQ, T_GT, T_LT]
        conditionComp = [T_ADD, T_SUB]
        conditionBoolean = [T_AND, T_OR]

        if command in conditionCmp:
            n = self._UniqueLabel()
            text = ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "D=M-D", "@T_JUMP" + n, "@F_JUMP" + n, "0;JMP",
                    "(T_JUMP" + n + ")", "@SP", "A=M", "M=-1", "@END" + n, "0;JMP", "(F_JUMP" + n + ")", "@SP", "A=M", "M=0", "(END" + n + ")", "@SP", "M=M+1"]

        elif command in conditionComp or conditionBoolean:
            text = ["@SP", "AM=M-1", "D=M", "@SP",
                    "AM=M-1", "@SP", "M=M+1"]

        if T_ADD == command:
            text.insert(5, "M=M+D")
        elif T_SUB == command:
            text.insert(5, "M=M-D")
        elif T_NEG == command:
            text = ["@SP", "A=M-1", "M=-M"]
        elif T_EQ == command:
            text.insert(7, "D;JEQ")
        elif T_GT == command:
            text.insert(7, "D;JGT")
        elif T_LT == command:
            text.insert(7, "D;JLT")
        elif T_AND == command:
            text.insert(5, "M=D&M")
        elif T_OR == command:
            text.insert(5, "M=D|M")
        elif T_NOT == command:
            text = ["@SP", "A=M-1", "M=!M"]

        newline = '\n'
        code = newline.join(text)

        self._WriteCode(code)

    def WriteInit(self, sysinit=True):
        """
        Write the VM initialization code:
        To be implemented as part of Project 7
        """
        text = ["@256", "D=A", "@SP", "M=D"]
        newline = '\n'
        code = newline.join(text)
        self._WriteCode(code)

        if sysinit:
            self.WriteCall("Sys.init", '0')

        if (debug):
            self.file.write('    // Initialization code\n')

    def WriteLabel(self, label):
        """
        Write Hack code for 'label' VM command.
        To be implemented as part of Project 7

        """

        self._WriteCode("(" + label + ")")

    def WriteGoto(self, label):
        """
        Write Hack code for 'goto' VM command.
        To be implemented as part of Project 7
        """
        text = ["@" + label, "0;JMP"]

        newline = '\n'
        code = newline.join(text)

        self._WriteCode(code)

    def WriteIf(self, label):
        """
        Write Hack code for 'if-goto' VM command.
        To be implemented as part of Project 7
        """
        text = ["@SP", "AM=M-1", "D=M", "M=0", "@" + label, "D;JNE"]

        newline = '\n'
        code = newline.join(text)

        self._WriteCode(code)

    def WriteFunction(self, functionName, numLocals):
        """
        Write Hack code for 'function' VM command.
        To be implemented as part of Project 7
        """

        text = ["(" + functionName + ")", ]
        for i in range(int(numLocals)):
            text.extend(['@0', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

    def WriteReturn(self):
        """
        Write Hack code for 'return' VM command.
        To be implemented as part of Project 7
        """
        n = [('5', 'Return'), ('1', 'THAT'),
             ('2', 'THIS'), ('3', 'ARG'), ('4', 'LCL')]
        newline = '\n'
        text = ["@LCL", "D=M"]

        for x, y in n:
            if y == 'Return':
                text.extend(["@FRAME", "AM=D"])
            else:
                text.extend(["@FRAME", "D=M"])

            text.extend(["@" + x, "A=D-A", "D=M", "@" + y, "M=D"])
            if x == '5':
                code = newline.join(text)
                self._WriteCode(code)
                self.WritePushPop(3, 'argument', 0)
                text = ["@ARG", "D=M", "@SP", "M=D+1"]
                code = newline.join(text)
                self._WriteCode(code)
                text = []

        text.extend(["@Return", "A=M", "0;JMP"])

        newline = '\n'
        code = newline.join(text)
        self._WriteCode(code)

    def WriteCall(self, functionName, numArgs):
        """
        Write Hack code for 'call' VM command.
        To be implemented as part of Project 7
        """
        newline = '\n'
        fName = functionName + "_" + str(numArgs)
        self._WriteCode("@" + fName)
        text = ["D=A", "@SP", "A=M", "M=D", "@SP", "M = M + 1"]
        code = newline.join(text)
        self._WriteCode(code)
        self.WritePushPop(2, 'local', 'CALL')
        self.WritePushPop(2, 'argument', 'CALL')
        self.WritePushPop(2, 'this', 'CALL')
        self.WritePushPop(2, 'that', 'CALL')
        text = ["@SP", "D=M", "@" +
                str(numArgs), "D=D-A", "@5", "D=D-A", "@ARG", "M=D", "@SP, D=M, @LCL", "M=D"]

        code = newline.join(text)
        self._WriteCode(code)
        self.WriteGoto(fName)
        self.WriteLabel(fName)
