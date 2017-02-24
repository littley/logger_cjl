class PseudoStream(object):
    """
    This class is substituted for sys.stdout and sys.stderr
    """
    def __init__(self, target_stream, echo=False, store=False, output_file=None, append=True):
        self._trueStream = target_stream
        self._echo = echo
        self._store = store
        self._output_file = output_file
        self._out_fobj = None
        self._data = []
        if self._output_file is not None:
            mode = 'w'
            if append:
                mode = 'a'
            self._out_fobj = open(self._output_file, mode)

    def write(self,s):
        if self._echo:
            self._trueStream.write(s)
        if self._out_fobj is not None:
            self._out_fobj.write(s)
        if self._store:
            self._data.append(s)

    def __del__(self):
        if self._out_fobj is not None:
            self._out_fobj.close()

    def get_data(self):
        """
        Extract the data that has been captured (assuming it has been capturing in the first place)
        :return:
        """
        return self._data
