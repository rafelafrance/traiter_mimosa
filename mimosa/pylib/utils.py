"""Misc. utilities."""

import os
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Generator, Optional, Union


@contextmanager
def get_temp_dir(
    prefix: str = 'temp_',
    where: Optional[Union[str, Path]] = None,
    keep: bool = False
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
