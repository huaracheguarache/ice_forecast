import xarray as xr
from pyproj import CRS, Transformer
import numpy as np
from scipy.interpolate import RegularGridInterpolator

ds_topaz = xr.open_dataset(f'https://thredds.met.no/thredds/dodsC/accibergt5/topaz5_be_mem001.ncml')

start = np.datetime64(ds_topaz.bulletin_date) + np.timedelta64(12, 'h')
time = np.arange(start, start + np.timedelta64(10, 'D'), np.timedelta64(1, 'D'))
da_topaz = ds_topaz.siconc.sel(time=time)

crs_topaz = CRS.from_cf(ds_topaz.stereographic.attrs)

ds_regions = xr.open_dataset('regions_nh_ease2-250_sii-v3p0.nc')
crs_regions = CRS.from_cf(ds_regions.crs.attrs)

transformer = Transformer.from_crs(crs_topaz, crs_regions, always_xy=True)

# Converting to meters and creating a meshgrid.
x_topaz, y_topaz = np.meshgrid(da_topaz.x.values * 100_000, da_topaz.y.values * 100_000)
xt_topaz, yt_topaz = transformer.transform(xx=x_topaz, yy=y_topaz)

x_regions = ds_regions.xc.values * 1000
y_regions = ds_regions.yc.values * 1000

regions = ['centralarc', 'beaufort', 'chukchi', 'ess', 'laptev', 'kara', 'barents', 'greenland', 'baffin', 'lawrence',
           'hudson', 'canarch', 'bering', 'okhotsk', 'japan', 'bohai', 'baltic', 'alaska', 'fram', 'bar', 'sval']

for i, region in enumerate(regions):
    interp = RegularGridInterpolator((x_regions, y_regions), ds_regions.region_mask.isel(region=i).values,
                                     method='nearest')
    masked = interp((xt_topaz, yt_topaz)) * da_topaz

    resolution = 6.25  # kilometers
    area_per_cell = resolution ** 2  # square kilometers

    million_sq_km = 1_000_000
    sie_threshold = 0.15
    print((masked * area_per_cell).sum(dim=['x', 'y']) / million_sq_km)
    #(xr.where(da >= sie_threshold, 1, 0) * area_per_cell).sum(dim=['x', 'y']) / million_sq_km


