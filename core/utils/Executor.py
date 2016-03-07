import subprocess
import sys
import platform
import os

from core.exceptions.Exceptions import UnsupportedPlatformException


class Executor(object):
    def __init__(self, cwd, logfile='dune.log'):
        self.process = None
        self.cwd = cwd
        self.log = open(
            os.path.join(self.cwd, logfile),
            'ab'
        )

    def logged_call(self, cmd):
        if 'posix' not in sys.builtin_module_names:
            raise UnsupportedPlatformException

        cmd = _convert_subprocess_cmd(cmd)

        self.log = open(
            os.path.join(self.cwd, 'dune.log'),
            'ab'
        )

        try:
            self.process = subprocess.Popen(args=cmd,
                                            cwd=self.cwd,
                                            stdout=subprocess.PIPE,
                                            bufsize=1,
                                            close_fds=True)


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
                    # subprocess is still running
                    # TODO: This can be optimized by sleeping for a while
                    pass
            else:
                # Found some text in stdout

                # noinspection PyTypeChecker
                self.log.write(line)

                # Flush file object to ensure real-time logging
                self.log.flush()

    def is_running(self):
        return self.process.poll() is None

    def terminate(self):
        self.process.terminate()
        self.process.stdout.close()

    def close(self):
        # Close file handlers
        self.log.close()
        self.process.stdout.close()

    @property
    def pid(self):
        return self.process.pid


def _convert_subprocess_cmd(cmd):
    if platform.system() == 'Windows':
        raise UnsupportedPlatformException
    else:
        return [cmd]


def _perror(e):
    print("subprocess.CalledProcessError: Command '%s' returned non-zero exit status %s" % (
        ' '.join(e.cmd), str(e.returncode)))

    # TODO: Implement cleanup()
    # Communicate return code to the calling program if any
    sys.exit(e.returncode)


def call(cmd, cwd):
    cmd = _convert_subprocess_cmd(cmd)
    try:
        subprocess.check_call(cmd,
                              cwd=cwd,
                              shell=False,
                              stdin=subprocess.PIPE,
                              stdout=None,
                              stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        _perror(e)


def check_output(cmd, cwd):
    cmd = _convert_subprocess_cmd(cmd)
    try:
        out = subprocess.check_output(cmd,
                                      cwd=cwd,
                                      shell=False,
                                      stdin=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        _perror(e)
    finally:
        return out
