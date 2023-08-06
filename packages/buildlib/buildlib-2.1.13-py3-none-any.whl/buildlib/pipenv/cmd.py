from cmdi import CmdResult, command, set_result, strip_args
import subprocess as sp

from . import lib


@command
def install(
    dev: bool = False,
    **cmdargs,
) -> CmdResult:
    lib.install(**strip_args(locals()))
    return set_result()


@command
def create_env(
    version: str,
    **cmdargs,
) -> CmdResult:
    lib.create_env(**strip_args(locals()))
    return set_result()
