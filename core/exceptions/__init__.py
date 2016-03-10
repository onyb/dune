class UnsupportedPlatformException(Exception):
    """
    Exeception raised for platforms unsupported by Dune
    """
    pass


class OPAMConfigurationError(Exception):
    """
    Exeception raised if OPAM configuration is not found
    """
    pass


class InsufficientPrivilegeError(Exception):
    """
    Exeception raised if API server is launched without sudo
    """
    pass


class UnikernelLibraryNotFound(Exception):
    """
    Exeception raised if the unikernel build tools are not found by the API server
    """
    pass