import xarray as xr
import numpy as np


ds = xr.open_dataset('https://thredds.met.no/thredds/dodsC/accibergt5/topaz5_be_mem001.ncml')

start = np.datetime64(ds.bulletin_date) + np.timedelta64(12, 'h')
time = np.arange(start, start + np.timedelta64(10, 'D'), np.timedelta64(1, 'D'))

da = ds.siconc.sel(time=time)

area_per_cell = 100 * 100 # square kilometers

sia = (da * area_per_cell).sum(dim=['x', 'y']) / 1_000_000
sie = (xr.where(da >= 0.15, 1, 0) * area_per_cell).sum(dim=['x', 'y']) / 1_000_000

print(sia)
print(sie)

# TODO: figure out why the forecasted area and extent is several orders of magnitude larger than what is observed.
