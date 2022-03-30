"""Misc. utilities."""
import os
import shutil
import tempfile
import typing
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def get_temp_dir(
    prefix: str = "temp_",
    where: typing.Optional[typing.Union[str, Path]] = None,
    keep: bool = False,
) -> typing.Generator:
    """Handle creation and deletion of temporary directory."""
    if where and not os.path.exists(where):
        os.mkdir(where)

    temp_dir = tempfile.mkdtemp(prefix=prefix, dir=where)

    try:
        yield temp_dir
    finally:
        if not keep or not where:
            shutil.rmtree(temp_dir)


def remove_traits(old_set: set, *remove: str) -> list:
    """Remove an element from a copy of the set."""
    removes = {r for r in remove}
    new_set = {e for e in old_set if e not in removes}
    return list(new_set)
