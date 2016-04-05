import os
import platform
import shlex
import subprocess
import sys
import time

from core.api.Status import Status
from core.exceptions import UnsupportedPlatformException


class Executor(object):
    def __init__(
            self,
            cwd: str
    ):
        self.process = None
        self.cwd = cwd

    def logged_call(
            self,
            cmd,
            logfile: str = 'dune.log',
            stderr: bool = False
    ):
        if 'posix' not in sys.builtin_module_names:
            raise UnsupportedPlatformException

        log = open(
            os.path.join(self.cwd, logfile),
            'ab'
        )

        cmd = _convert_subprocess_cmd(cmd)

        try:
            if not stderr:
                self.process = subprocess.Popen(
                    args=cmd,
                    cwd=self.cwd,
                    stdout=subprocess.PIPE,
                    bufsize=-1,
                    close_fds=True
                )
            else:
                self.process = subprocess.Popen(
                    args=cmd,
                    cwd=self.cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    bufsize=-1,
                    close_fds=True
                )

        except subprocess.CalledProcessError as e:
            _perror(e)

        while True:
            line = self.process.stdout.readline()
            if line == b'':
                # No output in stdout
                if not self.is_running():
                    # subprocess has completed execution
                    return  # TODO: Implement status codes
                else:
                    print("Running")
                    # subprocess is still running
                    # TODO: This can be optimized by sleeping for a while
                    pass
            else:
                # Found some text in stdout

                # noinspection PyTypeChecker
                log.write(line)

                # Flush file object to ensure real-time logging
                log.flush()
        log.close()

    def call(self, cmd):
        if 'posix' not in sys.builtin_module_names:
            raise UnsupportedPlatformException

        cmd = _convert_subprocess_cmd(cmd)

        try:
            self.process = subprocess.Popen(
                args=cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE
            )

        except subprocess.CalledProcessError as e:
            _perror(e)

    def probe_status(self):
        # FIXME: Pointless line to satisfy processor clock
        time.sleep(0.5)
        status = self.process.poll()
        if status is None:
            return Status.RUNNING
        elif status is 0:
            return Status.SUCCEEDED
        elif status < 0:
            return Status.KILLED
        else:
            # FIXME: Investigate more into this case
            return Status.FAILED

    def is_running(self) -> bool:
        # FIXME: Pointless line to satisfy processor clock
        time.sleep(0.5)
        return self.process.poll() is None

    def has_completed(self) -> bool:
        # FIXME: Pointless line to satisfy processor clock
        time.sleep(0.5)
        return self.process.poll() is 0

    def was_terminated(self) -> bool:
        # FIXME: Pointless line to satisfy processor clock
        time.sleep(0.5)
        return self.process.poll() < 0

    def terminate(self):
        self.process.terminate()
        self.process.stdout.close()

    def close(self):
        self.process.stdout.close()

    @property
    def pid(self) -> int:
        return self.process.pid


def _convert_subprocess_cmd(cmd):
    if platform.system() == 'Windows':
        raise UnsupportedPlatformException
    else:
        return shlex.split(cmd)


def _perror(e):
    print("subprocess.CalledProcessError: Command '%s' returned non-zero exit status %s" % (
        ' '.join(e.cmd), str(e.returncode)))

    # TODO: Implement cleanup()
    # Communicate return code to the calling program if any
    sys.exit(e.returncode)


def call(cmd, cwd):
    cmd = _convert_subprocess_cmd(cmd)
    try:
        subprocess.check_call(
            cmd,
            cwd=cwd,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=None,
            stderr=subprocess.STDOUT
        )

    except subprocess.CalledProcessError as e:
        _perror(e)


def check_output(
        cmd,
        cwd=os.getcwd(),
        strip=False
):
    cmd = _convert_subprocess_cmd(cmd)
    try:
        out = subprocess.check_output(
            cmd,
            cwd=cwd,
            shell=False,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).decode('utf-8')

    except subprocess.CalledProcessError as e:
        _perror(e)
    finally:
        if not strip:
            return out
        else:
            return out.strip()


def pidof(name):
    cmd = 'pidof ' + name
    out = check_output(
        cmd,
        strip=True
    )

    return int(out)
