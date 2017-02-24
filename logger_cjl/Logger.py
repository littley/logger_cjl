import sys
from PseudoStream import PseudoStream

class Logger(object):
        """
        Utility class for capturing and redirecting output
        """

        _true_stdout = None
        _false_stdout = None
        _true_stderr = None
        _false_stderr = None

        _is_capturing = False
        @property
        def is_capturing(self):
            return self._is_capturing

        _capture_stdout = None
        @property
        def capture_stdout(self):
            return self._capture_stdout
        @capture_stdout.setter
        def capture_stdout(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._capture_stdout = value

        _capture_stderr = None
        @property
        def capture_stderr(self):
            return self._capture_stderr
        @capture_stderr.setter
        def capture_stderr(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._capture_stderr = value

        _echo_stdout = None
        @property
        def echo_stdout(self):
            return self._echo_stdout
        @echo_stdout.setter
        def echo_stdout(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._echo_stdout = value

        _echo_stderr = None
        @property
        def echo_stderr(self):
            return self._echo_stderr
        @echo_stderr.setter
        def echo_stderr(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._echo_stderr = value

        _store_stdout = None
        @property
        def store_stdout(self):
            return self._store_stdout
        @store_stdout.setter
        def store_stdout(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._store_stdout = value

        _store_stderr = None
        @property
        def store_stderr(self):
            return self._store_stderr
        @store_stderr.setter
        def store_stderr(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._store_stderr = value

        _file_for_stdout = None
        @property
        def file_for_stdout(self):
            return self._file_for_stdout
        @file_for_stdout.setter
        def file_for_stdout(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._file_for_stdout = value

        _file_for_stderr = None
        @property
        def file_for_stderr(self):
            return self._file_for_stderr
        @file_for_stderr.setter
        def file_for_stderr(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._file_for_stderr = value

        _append_to_stdout_file = None
        @property
        def append_to_stdout_file(self):
            return self._append_to_stdout_file
        @append_to_stdout_file.setter
        def append_to_stdout_file(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._append_to_stdout_file = value

        _append_to_stderr_file = None
        @property
        def append_to_stderr_file(self):
            return self._append_to_stderr_file
        @append_to_stderr_file.setter
        def append_to_stderr_file(self, value):
            if self._is_capturing:
                raise Exception('cannot modify this property while capturing output')
            self._append_to_stderr_file = value

        _stdout_data = None
        @property
        def stdout_data(self):
            """
            Use this property to access everything that has been accumulated in the stdout buffer
            """
            if self._is_capturing:
                return self._false_stdout.get_data()
            else:
                return self._stdout_data

        _stderr_data = None
        @property
        def stderr_data(self):
            """
            Use this property to access everything that has accumulated in the stderr buffer
            """
            if self._is_capturing:
                return self._false_stderr.get_data()
            else:
                return self._stderr_data

        def __init__(self,
                     capture_stdout=True,
                     capture_stderr=True,
                     echo_stdout=True,
                     echo_stderr=True,
                     store_stdout=False,
                     store_stderr=False,
                     file_for_stdout=None,
                     file_for_stderr=None,
                     append_to_stdout_file=True,
                     append_to_stderr_file=True):
            """
            :param capture_stdout: if True then all values written to stdout will be captured
            :param capture_stderr: if True then all values written to stderr will be captured
            :param echo_stdout: if True and stdout is being captured then print values written to stdout
            :param echo_stderr: if True and stderr is being captured then print values written to stderr
            :param store_stdout: if True and stdout is being captured then _store stdout in a list
            :param store_stderr: if True and stderr is being captured then _store stderr in a list
            :param file_for_stdout: if not None and stdout is being captured then write stdout to this file
            :param file_for_stderr: if not None and stderr is being captured then write stderr to this file
            :param append_to_stdout_file: if True then do not overwrite the file used to store stdout
            :param append_to_stderr_file: if True then do not overwrite the file used to store stderr
            """

            self._true_stdout = sys.stdout
            self._false_stdout = None
            self._true_stderr = sys.stderr
            self._false_stderr = None

            self._is_capturing = False

            self._capture_stdout = capture_stdout
            self._capture_stderr = capture_stderr
            self._echo_stdout = echo_stdout
            self._echo_stderr = echo_stderr
            self._store_stdout = store_stdout
            self._store_stderr = store_stderr
            self._file_for_stdout = file_for_stdout
            self._file_for_stderr = file_for_stderr
            self._append_to_stdout_file = append_to_stdout_file
            self._append_to_stderr_file = append_to_stderr_file

            self._stdout_data = None
            self._stderr_data = None

        def begin_capture(self):
            """
            Call this function to begin capturing output
            """
            self._is_capturing = True
            if self._capture_stdout:
                self._false_stdout = PseudoStream(sys.stdout,
                                                  echo=self._echo_stdout,
                                                  store=self._store_stdout,
                                                  output_file=self._file_for_stdout,
                                                  append=self._append_to_stdout_file)
                sys.stdout = self._false_stdout

            if self._capture_stderr:
                self._false_stderr = PseudoStream(sys.stderr,
                                                  echo=self._echo_stderr,
                                                  store=self._store_stderr,
                                                  output_file=self._file_for_stderr,
                                                  append=self._append_to_stderr_file)
                sys.stderr = self._false_stderr

        def end_capture(self):
            """
            Call this function to stop capturing output
            """
            self._is_capturing = False
            self._stdout_data = self._false_stdout.get_data()
            self._stderr_data = self._false_stderr.get_data()

            sys.stdout = self._true_stdout
            sys.stderr = self._true_stderr

            self._false_stdout = None
            self._false_stderr = None
