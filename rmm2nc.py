import numpy as np
import datetime as dt
from netCDF4 import Dataset

fn = 'rmm.74toRealtime.txt'

# Read ascii data and assign columns to data
D = np.array(np.loadtxt(fn, skiprows=2, usecols=range(7)))

year = D[:,0]
month = D[:,1]
day = D[:,2]
rmm1 = D[:,3]
rmm2 = D[:,4]
phase = D[:,5]
amplitude = D[:,6]

# Handle missing/invalud data values
rmm1[rmm1 > 100] = np.nan
rmm2[rmm2 > 100] = np.nan
phase[phase > 100] = np.nan
amplitude[amplitude > 100] = np.nan

# Deal with time.
nc_timestamp = np.array(
    [(dt.datetime(int(year[ii]),
                  int(month[ii]),
                  int(day[ii]),
                  0, 0, 0)
      - dt.datetime(1970,1,1,0,0,0)
      ).total_seconds()/3600.0 for ii in range(len(year))]
)

# Write out to NetCDF format.
fn_out = 'rmm.nc'

with Dataset(fn_out, 'w') as DS:

    DS.createDimension('time',len(year))

    DS.createVariable('time', 'd', ('time',))
    DS.createVariable('year', 'd', ('time',))
    DS.createVariable('month', 'd', ('time',))
    DS.createVariable('day', 'd', ('time',))
    DS.createVariable('rmm1', 'd', ('time',))
    DS.createVariable('rmm2', 'd', ('time',))
    DS.createVariable('phase', 'd', ('time',))
    DS.createVariable('amplitude', 'd', ('time',))

    DS['time'][:] = nc_timestamp
    DS['time'].units = 'hours since 1970-1-1 00:00 UTC'
    DS['year'][:] = year
    DS['month'][:] = month
    DS['day'][:] = day
    DS['rmm1'][:] = rmm1
    DS['rmm2'][:] = rmm2
    DS['phase'][:] = phase
    DS['amplitude'][:] = amplitude
