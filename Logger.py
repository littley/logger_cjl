import sys

class Logger(object):
        """
        Utility class for capturing and redirecting output
        """
        def __init__(self,
                     captureSTDOUT=True,
                     captureSTDERR=True,
                     echoSTDOUT=True,
                     echoSTDERR=True,
                     storeSTDOUT=False,
                     storeSTDERR=False,
                     fileForSTDOUT=None,
                     fileForSTDERR=None):
            """
            :param captureSTDOUT: if True then all values written to stdout will be captured
            :param captureSTDERR: if True then all values written to stderr will be captured
            :param echoSTDOUT: if True and stdout is being captured then print values written to stdout
            :param echoSTDERR: if True and stderr is being captured then print values written to stderr
            :param storeSTDOUT: if True and stdout is being captured then store stdout in a list
            :param storeSTDERR: if True and stderr is being captured then store stderr in a list
            :param fileForSTDOUT: if not None and stdout is being captured then write stdout to this file
            :param fileForSTDERR: if not None and stderr is being captured then write stderr to this file
            """

            self._trueSTDOUT = sys.stdout
            self._falseSTDOUT = None
            self._trueSTDERR = sys.stderr
            self._falseSTDERR = None

            self.isCapturing = False

            self._captureSTDOUT = captureSTDOUT
            self._captureSTDERR = captureSTDERR
            self._echoSTDOUT = echoSTDOUT
            self._echoSTDERR = echoSTDERR
            self._storeSTDOUT = storeSTDOUT
            self._storeSTDERR = storeSTDERR
            self._fileForSTDOUT = fileForSTDOUT
            self._fileForSTDERR = fileForSTDERR

            self._data_STDOUT = None
            self._data_STDERR = None

        def setFileForSTDOUT(self, fileName):
            """
            Change the file where stdout is written.  Cannot be modified during a capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change output file while capturing output!")
            self._fileForSTDOUT = fileName

        def setFileForSTDERR(self, fileName):
            """
            Change the file where stderr is written.  Cannot be modified during a capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change output file while capturing output!")
            self._fileForSTDERR = fileName

        def setCaptureSTDOUT(self, newValue):
            """
            Toggle the capture of stdout.  Cannot be modified during capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change this value file while capturing output!")
            self._captureSTDOUT = newValue

        def setCaptureSTDERR(self, newValue):
            """
            Toggle the capture of stderr.  Cannot be modified during capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change this value file while capturing output!")
            self._captureSTDERR = newValue

        def setEchoSTDOUT(self, newValue):
            """
            Toggle the printing of stdout.  Cannot be modified during capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change this value file while capturing output!")
            self._echoSTDOUT = newValue

        def setEchoSTDERR(self, newValue):
            """
            Toggle the printing of stderr.  Cannot be modified during capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change this value file while capturing output!")
            self._echoSTDERR = newValue

        def setStoreSTDOUT(self, newValue):
            """
            Toggle the storing of stdout.  Cannot be modified during capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change this value file while capturing output!")
            self._storeSTDOUT = newValue

        def setStoreSTDERR(self, newValue):
            """
            Toggle the storing of stderr.  Cannot be modified during capture.
            """
            if self.isCapturing:
                raise Exception("Error: cannot change this value file while capturing output!")
            self._storeSTDERR = newValue

        def getSTDOUT(self):
            """
            If a stdout has been stored then the result can be retrieved by this function.  Returns a list of lines.
            """
            if self.isCapturing:
                return self._falseSTDOUT.getData()
            else:
                return self._data_STDOUT

        def getSTDERR(self):
            """
            If a stderr has been stored then the result can be retrieved by this function.  Returns a list of lines.
            """
            if self.isCapturing:
                return self._falseSTDERR.getData()
            else:
                return self._data_STDERR

        def beginCapture(self):
            """
            Call this function to begin capturing output
            """
            self.isCapturing = True
            if self._captureSTDOUT:
                self._falseSTDOUT = _stream(sys.stdout, echo=self._echoSTDOUT,
                                           store=self._storeSTDOUT, outputFile=self._fileForSTDOUT)
                sys.stdout = self._falseSTDOUT

            if self._captureSTDERR:
                self._falseSTDERR = _stream(sys.stderr, echo=self._echoSTDERR,
                                           store=self._storeSTDERR, outputFile=self._fileForSTDERR)
                sys.stderr = self._falseSTDERR

        def endCapture(self):
            """
            Call this function to stop capturing output
            """
            self.isCapturing = False
            self._data_STDOUT = self._falseSTDOUT.getData()
            self._data_STDERR = self._falseSTDERR.getData()

            sys.stdout = self._trueSTDOUT
            sys.stderr = self._trueSTDERR

            self._falseSTDOUT = None
            self._falseSTDERR = None




class _stream(object):
    """
    This class is substituted for sys.stdout and sys.stderr
    """
    def __init__(self, targetStream, echo=False, store=False, outputFile=None):
        self._trueStream = targetStream
        self.echo = echo
        self.store = store
        self.outputFile = outputFile
        self.outFOBJ = None
        self.data = []
        if self.outputFile is not None:
            self.outFOBJ = open(self.outputFile, "w")

    def write(self,s):
        if self.echo:
            self._trueStream.write(s)
        if self.outFOBJ is not None:
            self.outFOBJ.write(s)
        if self.store:
            self.data.append(s)

    def __del__(self):
        if self.outFOBJ is not None:
            self.outFOBJ.close()

    def getData(self):
        """
        Extract the data that has been captured (assuming it has been capturing in the first place)
        :return:
        """
        return self.data