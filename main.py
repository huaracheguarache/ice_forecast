from pathlib import Path
import xarray as xr
import numpy as np


p = Path('data')
p.mkdir(exist_ok=True)


sia = []
sie = []
for i in range(1, 11):
    ds = xr.open_dataset(f'https://thredds.met.no/thredds/dodsC/accibergt5/topaz5_be_mem0{i:02}.ncml')

    start = np.datetime64(ds.bulletin_date) + np.timedelta64(12, 'h')
    time = np.arange(start, start + np.timedelta64(10, 'D'), np.timedelta64(1, 'D'))

    da = ds.siconc.sel(time=time)

    resolution = 6.25  # kilometers
    area_per_cell = resolution**2  # square kilometers

    million_sq_km = 1_000_000
    sie_threshold = 0.15
    sia.append((da * area_per_cell).sum(dim=['x', 'y']) / million_sq_km)
    sie.append((xr.where(da >= sie_threshold, 1, 0) * area_per_cell).sum(dim=['x', 'y']) / million_sq_km)

ds_sia = xr.concat(sia, dim=xr.Variable('member', [i for i in range(1, 11)])).convert_calendar('all_leap')
ds_sia.to_netcdf(p / 'sia_nh.nc')
ds_sie = xr.concat(sie, dim=xr.Variable('member', [i for i in range(1, 11)])).convert_calendar('all_leap')
ds_sie.to_netcdf(p / 'sie_nh.nc')

# TODO: implement region masking
