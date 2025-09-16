from pathlib import Path
import xarray as xr
from pyproj import CRS, Transformer
import numpy as np
from scipy.interpolate import NearestNDInterpolator


p = Path('data')
p.mkdir(exist_ok=True)

members = []
for i in range(1, 11):
    members.append(xr.open_dataset(f'https://thredds.met.no/thredds/dodsC/accibergt5/topaz5_be_mem0{i:02}.ncml'))

crs_topaz = CRS.from_cf(members[0].stereographic.attrs)

ds_regions = xr.open_dataset('regions_nh_ease2-250_sii-v3p0.nc')
crs_regions = CRS.from_cf(ds_regions.crs.attrs)

transformer = Transformer.from_crs(crs_topaz, crs_regions, always_xy=True)

# Converting to meters and creating a meshgrid.
x_topaz, y_topaz = np.meshgrid(members[0].x.values * 100_000, members[0].y.values * 100_000)
xt_topaz, yt_topaz = transformer.transform(xx=x_topaz, yy=y_topaz)

x_regions = ds_regions.xc.values * 1000
y_regions = ds_regions.yc.values * 1000

interp = NearestNDInterpolator(list(zip(y_regions, x_regions)), ds_regions.region_mask.isel(region=0).values)
mask = interp(yt_topaz, xt_topaz)

regions = ['centralarc', 'beaufort', 'chukchi', 'ess', 'laptev', 'kara', 'barents', 'greenland', 'baffin', 'lawrence',
           'hudson', 'canarch', 'bering', 'okhotsk', 'japan', 'bohai', 'baltic', 'alaska', 'fram', 'bar', 'sval']




"""
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
"""