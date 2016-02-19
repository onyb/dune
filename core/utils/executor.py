import subprocess
import sys
import platform
import os


def _convert_subprocess_cmd(cmd):
    if platform.system() == 'Windows':
        if '"' in cmd:
            # Assume there's only one quoted argument.
            bits = cmd.split('"')
            return bits[0].split() + [bits[1]] + bits[2].split()
        else:
            return cmd.split()
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
                              shell=True,
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
                                      shell=True,
                                      stdin=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        _perror(e)
    finally:
        return out


def logged_call(cmd, cwd):
    cmd = _convert_subprocess_cmd(cmd)

    log = open(
        os.path.join(cwd, 'dune.log'),
        'a'
    )

    try:
        with subprocess.Popen(cmd,
                              cwd=cwd,
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True) as p:
            for line in p.stdout:
                log.write(line)

    except subprocess.CalledProcessError as e:
        _perror(e)

    finally:
        log.close()
