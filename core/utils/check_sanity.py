import subprocess

import os

from core.utils.Executor import _convert_subprocess_cmd, pidof


def check_environment() -> bool:
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
    try:
        subprocess.check_output(
            _convert_subprocess_cmd('which mirage')
        )

    except subprocess.CalledProcessError:
        return False
    else:
        return True


def check_redis_server() -> bool:
    try:
        pidof('redis-server')

    except subprocess.CalledProcessError as e:
        return False
    else:
        return True


def check_redis_queue() -> bool:
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


def is_root() -> bool:
    # Get the effective user id
    if os.geteuid() == 0:
        return True
    else:
        return False
