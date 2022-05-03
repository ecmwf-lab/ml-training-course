#!/usr/bin/env python

import climetlab as cml
ds = cml.load_source("url", "https://github.com/ecmwf/climetlab/raw/main/docs/examples/test.nc")
data = ds.to_xarray()
print(data)
