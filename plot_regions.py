import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmcrameri.cm as cmc

ds_regions = xr.open_dataset('regions_nh_ease2-250_sii-v3p0.nc')

x_regions = ds_regions.xc.values * 1000
y_regions = ds_regions.yc.values * 1000
X, Y = np.meshgrid(x_regions, y_regions)


crs = ccrs.LambertAzimuthalEqualArea(central_longitude=0.0, central_latitude=90)
ax = plt.axes(projection=crs)
ax.coastlines()

regions = ['centralarc', 'beaufort', 'chukchi', 'ess', 'laptev', 'kara', 'barents', 'greenland', 'baffin', 'lawrence',
           'hudson', 'canarch', 'bering', 'okhotsk', 'japan', 'bohai', 'baltic', 'alaska', 'fram', 'bar', 'sval']

colours = cmc.batlow(np.linspace(0, 1, len(regions)))
for i, region in enumerate(regions):
    one_region = ds_regions.region_mask.isel(region=i)
    values = one_region.where(one_region == 1).values
    ax.scatter(X, Y, values, c=colours[i], transform=crs)

plt.show()
