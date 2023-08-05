# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

""" CliMetLab plugins rely on the python plugins_ system using ``entry_points``.

.. _plugins: https://packaging.python.org/guides/creating-and-discovering-plugins/

"""

import logging
import os
from collections import defaultdict
from importlib import import_module
from typing import List, Union

import entrypoints

import climetlab

from .settings import SETTINGS

LOG = logging.getLogger(__name__)

CACHE = {}

PLUGINS = {}

REGISTERED = defaultdict(dict)


def register(kind, name_or_module, module_or_none=None):
    """Register a plugin manually.

    When installing a plugin (for instance with `!pip install` in a notebook), the pip package with register the plugin with the `entry_points` mechanism, but the currently runnning kernel will need to be restarted to take the change into account. Using :py:func:`register` alleviates this issue.

    Parameters
    ----------
    kind : str
        Type of plugind.
    name_or_module : str or module
        Name of the installed plugin to registed.
    module_or_none : module, optional
        Module recently installed to be registered.

    """  # noqa: E501

    if isinstance(name_or_module, str):
        name = name_or_module
        module = module_or_none
    else:
        assert module_or_none is None, (
            f"Value of module_or_none({module_or_none}) is ignored when "
            + "name_or_module ({name_or_module}) is not of type str."
        )
        module = name_or_module
        name = module.__name__.replace("_", "-")
    REGISTERED[kind][name] = module


def _load_plugins(kind):
    plugins = {}
    for e in entrypoints.get_group_all(f"climetlab.{kind}s"):
        plugins[e.name.replace("_", "-")] = e
    return plugins


def load_plugins(kind):
    """Loads the plugins for a given kind. The plugin needs to have registered itself with entry_point.

    Parameters
    ----------
    kind : str
        Plugin type such as "dataset" or "source".
    """
    if PLUGINS.get(kind) is None:
        PLUGINS[kind] = _load_plugins(kind)
    return PLUGINS[kind]


def find_plugin(directories: Union[str, List[str]], name: str, loader):
    """Find a plugin by name .

    Parameters
    ----------
    directories : list or str
        List of directories to be searched to find the plugin.
    name : str
        Name of the plugin
    loader : class
        Class implementing load_yaml() and load_module()

    Returns
    -------
    Return what the loader will returns when applied to the plugin with the right name `name`, found in one of the directories of the `directories` list.

    Raises
    ------
    NameError
        If plugin is not found.
    """  # noqa: E501
    candidates = set()

    if name in REGISTERED[loader.kind]:
        return getattr(REGISTERED[loader.kind][name], loader.kind)

    candidates.update(REGISTERED[loader.kind].keys())

    plugins = load_plugins(loader.kind)

    if name in plugins:
        plugin = plugins[name]
        return loader.load_entry(plugin)

    candidates.update(plugins.keys())

    if not isinstance(directories, (tuple, list)):
        directories = [directories]

    for directory in directories:
        n = len(directory)
        for path, _, files in os.walk(directory):
            path = path[n:]
            for f in files:
                base, ext = os.path.splitext(f)
                if ext == ".yaml":
                    candidates.add(base)
                    if base == name:
                        full = os.path.join(directory, path, f)
                        return loader.load_yaml(full)

                if ext == ".py" and base[0] != "_":

                    full = os.path.join(path, base)
                    if full[0] != "/":
                        full = "/" + full
                    p = full[1:].replace("/", "-").replace("_", "-")
                    candidates.add(p)
                    if p == name:
                        return loader.load_module(full.replace("/", "."))

    candidates = ", ".join(sorted(c for c in candidates if "-" in c))
    raise NameError(f"Cannot find {loader.kind} '{name}' (values are: {candidates})")


def directories(owner: bool = False) -> list:
    """Return a list of directories that are used in the project .

    If owner = False, return a list of directories where to search for plugins.

    If owner = True, return a list of 2-uples to include the owner in the return value.

    Parameters
    ----------
    owner : bool, optional

    """

    result = []
    for conf in (
        "styles-directories",
        "projections-directories",
        "layers-directories",
        "datasets-directories",
    ):
        for d in SETTINGS.get(conf):
            if os.path.exists(d) and os.path.isdir(d):
                result.append(("user-settings", d))

    for kind in ("dataset", "source"):
        for name, v in load_plugins(kind).items():
            try:
                module = import_module(v.module_name)
                result.append((name, os.path.dirname(module.__file__)))
            except Exception:
                LOG.error("Cannot load module %s", v.module_name, exc_info=True)

    result.append(("climetlab", os.path.dirname(climetlab.__file__)))

    if owner:
        return result

    return [x[1] for x in result]
