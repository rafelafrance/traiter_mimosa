"""Misc. utilities."""
import os
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Generator
from typing import Optional
from typing import Union


@contextmanager
def get_temp_dir(
    prefix: str = "temp_", where: Optional[Union[str, Path]] = None, keep: bool = False
) -> Generator:
    """Handle creation and deletion of temporary directory."""
    if where and not os.path.exists(where):
        os.mkdir(where)

    temp_dir = mkdtemp(prefix=prefix, dir=where)

    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir)


def remove_traits(old_set: set, *remove: str) -> list:
    """Remove an element from a copy of the set."""
    removes = {r for r in remove}
    new_set = {e for e in old_set if e not in removes}
    return list(new_set)
