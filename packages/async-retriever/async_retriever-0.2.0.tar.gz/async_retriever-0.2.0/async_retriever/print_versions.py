"""Utility functions for printing version information.

The original script is from
`xarray <https://github.com/pydata/xarray/blob/master/xarray/util/print_versions.py>`__
"""
import importlib
import locale
import os
import platform
import struct
import subprocess
import sys
from typing import IO, List, Optional, Tuple


def get_sys_info() -> List[Tuple[str, Optional[str]]]:
    """Return system information as a dict.

    From https://github.com/numpy/numpy/blob/master/setup.py#L64-L89

    Returns
    -------
    list
        System information such as python version.
    """
    blob = []

    def _minimal_ext_cmd(cmd: List[str]) -> bytes:
        # construct minimal environment
        env = {}
        for k in ["SYSTEMROOT", "PATH", "HOME"]:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env["LANGUAGE"] = "C"
        env["LANG"] = "C"
        env["LC_ALL"] = "C"
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, env=env)
        return out

    commit = None
    try:
        out = _minimal_ext_cmd(["git", "rev-parse", "HEAD"])
        commit = out.strip().decode("ascii")
    except (subprocess.SubprocessError, OSError):
        pass

    blob.append(("commit", commit))

    (sysname, _, release, _, machine, processor) = platform.uname()
    blob.extend(
        [
            ("python", sys.version),
            ("python-bits", f"{struct.calcsize('P') * 8}"),
            ("OS", f"{sysname}"),
            ("OS-release", f"{release}"),
            ("machine", f"{machine}"),
            ("processor", f"{processor}"),
            ("byteorder", f"{sys.byteorder}"),
            ("LC_ALL", f'{os.environ.get("LC_ALL", "None")}'),
            ("LANG", f'{os.environ.get("LANG", "None")}'),
            ("LOCALE", ".".join(str(i) for i in locale.getlocale())),
        ]
    )

    return blob


def show_versions(file: IO = sys.stdout) -> None:
    """Print the versions of pygeohydro stack and its dependencies.

    Parameters
    ----------
    file : file-like, optional
        print to the given file-like object. Defaults to sys.stdout.
    """
    sys_info = get_sys_info()

    deps = [
        # (MODULE_NAME, f(mod) -> mod version)
        ("async_retriever", lambda mod: mod.__version__),
        # dependencies
        ("orjson", lambda mod: mod.__version__),
        ("requests", lambda mod: mod.__version__),
        ("aiohttp", lambda mod: mod.__version__),
        ("cytoolz", lambda mod: mod.__version__),
        ("nest-asyncio", lambda mod: mod.__version__),
        ("aiohttp-client-cache", lambda mod: mod.__version__),
        ("aiosqlite", lambda mod: mod.__version__),
        # setup/test
        ("setuptools", lambda mod: mod.__version__),
        ("pip", lambda mod: mod.__version__),
        ("conda", lambda mod: mod.__version__),
        ("mamba", lambda mod: mod.__version__),
        ("pytest", lambda mod: mod.__version__),
    ]

    deps_blob: List[Tuple[str, Optional[str]]] = []
    for (modname, ver_f) in deps:
        try:
            if modname in sys.modules:
                mod = sys.modules[modname]
            else:
                mod = importlib.import_module(modname)
        except ModuleNotFoundError:
            deps_blob.append((modname, None))
        else:
            try:
                ver = ver_f(mod)
                deps_blob.append((modname, ver))
            except NotImplementedError:
                deps_blob.append((modname, "installed"))

    print("\nINSTALLED VERSIONS", file=file)
    print("------------------", file=file)

    for k, stat in sys_info:
        print(f"{k}: {stat}", file=file)

    print("", file=file)
    for k, stat in deps_blob:
        print(f"{k}: {stat}", file=file)
