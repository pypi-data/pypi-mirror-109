# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os
import warnings
import weakref
from importlib import import_module

from climetlab.core import Base
from climetlab.decorators import locked


class Reader(Base):
    def __init__(self, source, path):
        self._source = weakref.ref(source)
        self.path = path

    @property
    def source(self):
        return self._source()

    def mutate(self):
        # Give a chance to `directory` or `zip` to change the reader
        return self

    def sel(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def multi_merge(cls, readers):
        return None


class DefaultMerger:
    def __init__(self, engine, backend_kwargs):
        self.engine = engine
        self.backend_kwargs = backend_kwargs

    def merge(self, paths, **kwargs):
        import xarray as xr

        options = dict(backend_kwargs=self.backend_kwargs)
        options.update(kwargs)
        return xr.open_mfdataset(
            paths,
            engine=self.engine,
            **options,
        )


class MultiReaders(Base):
    backend_kwargs = {}

    def __init__(self, readers):
        self.readers = readers

    def to_xarray(self, merger=None, **kwargs):
        if merger is None:
            merger = DefaultMerger(self.engine, self.backend_kwargs)
        return merger.merge([r.path for r in self.readers], **kwargs)


_READERS = {}


# TODO: Add plugins
@locked
def _readers():
    if not _READERS:
        here = os.path.dirname(__file__)
        for path in os.listdir(here):
            if path.endswith(".py") and path[0] not in ("_", "."):
                name, _ = os.path.splitext(path)
                try:
                    _READERS[name] = import_module(f".{name}", package=__name__).reader
                except Exception as e:
                    warnings.warn(f"Error loading wrapper {name}: {e}")
    return _READERS


def reader(source, path):

    if os.path.isdir(path):
        from .directory import DirectoryReader

        return DirectoryReader(source, path).mutate()

    with open(path, "rb") as f:
        magic = f.read(8)

    for name, r in _readers().items():
        try:
            reader = r(source, path, magic)
            if reader is not None:
                return reader.mutate()
        except Exception as e:
            warnings.warn(f"Error calling reader '{name}': {e}")

    raise ValueError(f"Cannot find a reader for file '{path}' (magic {magic})")
