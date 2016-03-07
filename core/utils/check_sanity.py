import os
from core.utils.Executor import _convert_subprocess_cmd
import subprocess

from core.exceptions.Exceptions import OPAMConfigurationExeception


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
            raise OPAMConfigurationExeception

    PATH = os.environ.get('PATH')
    for path in PATH.split(':'):
        if path.endswith(
                os.path.join('.opam', 'system', 'bin')
        ):
            return True


def check_mirage():
    try:
        subprocess.check_call(
            _convert_subprocess_cmd('which mirage')
        )
    except subprocess.CalledProcessError:
        return False
    else:
        return True
