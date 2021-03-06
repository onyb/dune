import os
import subprocess

from core.utils.Executor import _convert_subprocess_cmd, pidof


def check_environment() -> bool:
    """
    Check if "opam config env" has set all the required environment variables

    :return: True for valid environment configuration and False otherwise
    """
    __opam_env__ = [
        'CAML_LD_LIBRARY_PATH',
        'MANPATH',
        'PERL5LIB',
        'OCAML_TOPLEVEL_PATH',
        'PATH'
    ]

    for var in __opam_env__:
        if not os.environ.get(var, None):
            return False

    PATH = os.environ.get('PATH')

    try:
        OCAML_VERSION = subprocess.check_output(
            _convert_subprocess_cmd('ocaml -vnum')
        ).decode('utf-8').strip()

    except subprocess.CalledProcessError:
        return False

    for path in PATH.split(':'):
        if path.endswith(
                os.path.join('.opam', 'system', 'bin')
        ) or path.endswith(
            os.path.join('.opam', OCAML_VERSION, 'bin')
        ):
            return True


def check_mirage() -> bool:
    """
    Check if MirageOS is installed by "opam"

    :return: True if dune can find "mirage", False otherwise
    """
    try:
        subprocess.check_output(
            _convert_subprocess_cmd('which mirage')
        )

    except subprocess.CalledProcessError:
        return False
    else:
        return True


def check_redis_server() -> bool:
    """
    Check if instance of Redis server is running

    :return: True if "redis-server" is running, False otherwise
    """
    pid = pidof('redis-server')

    if pid == -1:
        return False
    else:
        return True


def check_mongod_server() -> bool:
    """
    Check if instance of MongoDB server is running

    :return: True if "mongod" is running, False otherwise
    """
    pid = pidof('mongod')

    if pid == -1:
        return False
    else:
        return True


def check_redis_queue() -> bool:
    """
    Check if at least one worker is running in Python Redis Queue

    :return: True if at least 1 worker is running, False otherwise
    """
    try:
        out = subprocess.check_output(
            _convert_subprocess_cmd('rq info')
        ).decode('utf-8')

    except FileNotFoundError as e:
        return False
    else:
        if '0 workers' in out:
            return False

        return True


def check_privilege() -> bool:
    """
    Check if current user can execute apt-get on host without root access

    :return: True if apt-get is in sudoers list, False otherwise
    """
    try:
        out = subprocess.check_output(
            _convert_subprocess_cmd('sudo -l')
        ).decode('utf-8')

    except subprocess.CalledProcessError:
        pass
    else:
        # Check README.md for more details on how to add apt-get to sudoers list
        if 'User root' not in out and '(ALL : ALL) NOPASSWD: /usr/bin/apt-get install *' in out:
            return True
        else:
            return False


def is_not_root() -> bool:
    """
    Checks if current user is NOT "root"

    :return: True if effective user is NOT "root", False otherwise
    """
    if os.geteuid() == 0:
        return False
    else:
        return True
