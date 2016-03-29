#!/usr/bin/env python
import logging

from daemonize import Daemonize
from rq import Connection, Worker

from core.utils.Executor import check_output

__workers__ = [
    'alpha',
    'beta',
    'gamma',
    'delta',
    'epsilon',
    'zeta',
    'eta',
    'theta',
    'iota',
    'kappa',
    'lambda',
    'mu',
    'nu',
    'xi',
    'omicron',
    'pi',
    'rho',
    'sigma',
    'tau',
    'upsilon',
    'phi',
    'chi',
    'psi',
    'omega'
]


def get_available_worker_name():
    out = check_output(
        cmd='rq info',
        cwd='/'
    )
    for each in __workers__:
        if each not in out:
            return each

            # TODO: Raise exception for worker limit


def launch_worker():
    with Connection():
        w = Worker(
            get_available_worker_name()
        )

        w.work()


def launch_daemon():
    worker = get_available_worker_name()
    pid = "/tmp/%s.pid" % worker

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler("/tmp/%s.log" % worker, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]

    daemon = Daemonize(
        app="dune",
        pid=pid,
        action=launch_worker,
        keep_fds=keep_fds
    )

    daemon.start()
