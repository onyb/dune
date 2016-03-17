import subprocess

import os

from core.utils.Executor import _convert_subprocess_cmd


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
    for path in PATH.split(':'):
        if path.endswith(
                os.path.join('.opam', 'system', 'bin')
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


def check_redis_queue() -> bool:
    try:
        subprocess.check_output(
            _convert_subprocess_cmd('rq info')
        )

    except subprocess.CalledProcessError:
        return False
    else:
        return True


def is_root() -> bool:
    # Get the effective user id
    if os.geteuid() == 0:
        return True
    else:
        return False
