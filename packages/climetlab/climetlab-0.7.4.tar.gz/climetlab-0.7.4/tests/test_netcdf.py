#!/usr/bin/env python3

# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from climetlab import load_source, plot_map


def test_netcdf():
    for s in load_source("file", "docs/examples/test.nc"):
        plot_map(s)


def test_multi():
    s1 = load_source(
        "cds",
        "reanalysis-era5-single-levels",
        product_type="reanalysis",
        param="2t",
        date="2021-03-01",
        format="netcdf",
    )
    s1.to_xarray()
    s2 = load_source(
        "cds",
        "reanalysis-era5-single-levels",
        product_type="reanalysis",
        param="2t",
        date="2021-03-02",
        format="netcdf",
    )
    s2.to_xarray()

    source = load_source("multi", s1, s2)
    for s in source:
        print(s)

    source.to_xarray()


if __name__ == "__main__":
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            print(k)
            f()
