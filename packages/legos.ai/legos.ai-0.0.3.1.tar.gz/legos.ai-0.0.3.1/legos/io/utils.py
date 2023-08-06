import collections
from typing import Optional, Union
from pathlib import Path
Path.ls = lambda x: list(x.iterdir())

def ls(path: Optional[Union[str, Path]]):
    return path.ls()

def file_ext_counter(path: Optional[Union[str, Path]]):
    return collections.Counter(p.suffix for p in path.ls())

