import xarray as xr
from datetime import datetime
from netCDF4 import num2date, date2num


def load_data(input_file, lon_name='lon', lat_name='lat', time_name='time',
              add_initial_date=None, extent=None, period=None, ctime_unit=None, calendar_type=None, **kwargs):
    """
    Loads netCDF files and extracts data given a spatial extend and time period
    of interest.
    """
    # Open either single or multi-file data set depending if list of wildcard
    if "*" in input_file or isinstance(input_file, list):
        ds = xr.open_mfdataset(input_file, concat_dim=time_name, decode_times=False, autoclose=True,
                               chunks={time_name: 1})
    else:
        ds = xr.open_dataset(input_file, decode_times=False, autoclose=True, chunks={time_name: 1})

    if extent:
        south, north, west, east = extent

        ds = ds.where((ds[lat_name] >= south) & (ds[lat_name] <= north), drop=True)
        # Account for extent crossing Greenwich
        if west > east:
            ds = ds.where((ds[lon_name] >= west) | (ds[lon_name] <= east), drop=True)
        else:
            ds = ds.where((ds[lon_name] >= west) & (ds[lon_name] <= east), drop=True)

    # Construct condition base on time period
    if period:

        try:
            calendar = ds[time_name].calendar
        except AttributeError:
            calendar = calendar_type  # 'gregorian'
        except KeyError:
            calendar = calendar_type  # 'gregorian'

        try:
            time_units = ds[time_name].units
        except AttributeError:
            time_units = ctime_unit
        except KeyError:
            time_units = ctime_unit

        t1 = date2num(datetime(*period[0]), time_units, calendar)
        t2 = date2num(datetime(*period[1]), time_units, calendar)

        if add_initial_date is None:
            ds = ds.sel(time=(ds[time_name] >= t1) & (ds[time_name] <= t2))

        else:
            t0 = date2num(datetime(*add_initial_date), time_units, calendar)
            ds = ds.sel(time=(ds[time_name] + t0 >= t1) & (ds[time_name] + t0 <= t2))

    # Extra keyword arguments to select from additional dimensions (e.g. plev)
    if kwargs:
        ds = ds.sel(**kwargs)

    return ds
