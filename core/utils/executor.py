import subprocess
import sys
import platform
import os

from core.exceptions.Exceptions import UnsupportedPlatformException


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


def logged_call(cmd, cwd):
    global p
    if 'posix' not in sys.builtin_module_names:
        raise UnsupportedPlatformException

    cmd = _convert_subprocess_cmd(cmd)

    log = open(
        os.path.join(cwd, 'dune.log'),
        'ab'
    )

    try:
        p = subprocess.Popen(cmd,
                             cwd=cwd,
                             stdout=subprocess.PIPE,
                             bufsize=1,
                             close_fds=True)

    except subprocess.CalledProcessError as e:
        _perror(e)

    while True:
        line = p.stdout.readline()
        if line == b'':
            # No output in stdout
            if p.poll() is not None:
                # subprocess has completed execution
                break
            else:
                # subprocess is still running
                # TODO: This can be optimized by sleeping for a while
                pass
        else:
            # Found some text in stdout

            # noinspection PyTypeChecker
            log.write(line)

            # Flush file object to ensure real-time logging
            log.flush()

    # Clean up file handlers upon exit
    log.close()
    p.stdout.close()
