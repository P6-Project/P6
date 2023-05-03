from typing import Callable, Generator
import os
from pandas import DataFrame
from .utils import list_files

def extractor(extractPaths: dict[str, (Callable, bool, list[str])]) -> Generator[tuple[str, DataFrame], None, None]:
    for path, (func, nested, ext) in extractPaths.items():
        name = os.path.basename(os.path.splitext(path)[0])
        if nested:
            for path in list_files(path, ext):
                yield name, func(path)
        else:
            yield name, func(path)

def converter(extractPaths: dict[str, tuple[Callable, bool, list[str]]], dest: str, compressed: bool=False):
    ext = ".pkl" if not compressed else ".pkl.gz"
    compression = "gzip" if compressed else None
    for (name, df) in extractor(extractPaths):
        df.to_pickle(os.path.join(dest, name + ext), compression=compression)
