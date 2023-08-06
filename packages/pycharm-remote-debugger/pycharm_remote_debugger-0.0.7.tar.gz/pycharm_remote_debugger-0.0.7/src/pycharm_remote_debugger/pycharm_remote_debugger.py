import io
import runpy
import socket
import sys
from contextlib import redirect_stderr

import pydevd_pycharm
import waiting
from importlib.util import find_spec


class Options(object):
    mode = None
    address = None
    log_to = None
    log_to_stderr = False
    target = None  # unicode
    target_kind = None
    wait_for_client = False
    adapter_access_token = None


options = Options()
options.config = {"qt": "none", "subProcess": True}


class PycharmRemoteDebugger:
    DEFAULT_CONNECTION_TIMEOUT = 30

    def __init__(self, remote_machine: str, port: int, module: str, optional=False) -> None:
        self._remote_machine: str = remote_machine
        self._port: int = port
        self._module = module
        self._optional = optional

    def _debugger_login(self) -> bool:
        f = io.StringIO()

        with redirect_stderr(f):
            try:
                pydevd_pycharm.settrace(self._remote_machine, port=self._port, stdoutToServer=True, stderrToServer=True)
                return True
            except ConnectionRefusedError:
                return False

    def wait_for_debugger(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
        try:
            waiting.wait(
                lambda: self._debugger_login(),
                timeout_seconds=timeout,
                sleep_seconds=1,
                waiting_for="remote debugger to be ready"
            )
        except socket.timeout:
            if not self._optional:
                raise

        self.run_module()

    @classmethod
    def force_str(cls, s, encoding="ascii", errors="strict"):
        """Converts s to bytes, using the provided encoding. If s is already bytes,
        it is returned as is.
        If errors="strict" and s is bytes, its encoding is verified by decoding it;
        UnicodeError is raised if it cannot be decoded.
        """
        if isinstance(s, str):
            return s.encode(encoding, errors)
        else:
            s = bytes(s)
            if errors == "strict":
                # Return value ignored - invoked solely for verification.
                s.decode(encoding, errors)
            return s

    @classmethod
    def filename_str(cls, s, errors="strict"):

        return cls.force_str(s, sys.getfilesystemencoding(), errors)

    def run_module(self):
        argv = list(sys.argv)
        sys.path.insert(0, str(""))
        sys.argv = argv[argv.index("-m") + 1:]

        try:
            run_module_as_main = runpy._run_module_as_main
        except AttributeError:
            print("runpy._run_module_as_main is missing, falling back to run_module.")
            runpy.run_module(self._module[0], alter_sys=True)
        else:
            run_module_as_main(self._module[0], alter_argv=True)

        sys.argv = argv
