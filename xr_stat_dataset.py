import matplotlib.pyplot as plt
from dask.diagnostics import ProgressBar
from rw import load_data
import argparse
import datetime

display = False

parser = argparse.ArgumentParser(description='Performs statistcal analysis on dataset')

parser.add_argument("stat_function", help="statistical function to apply (tim_mean, spa_mean, "
                                          "tim_median, spa_median, tim_var, spa_var, "
                                          "tim_std, spa_std, tim_min, spa_min, tim_max, spa_max)")

parser.add_argument("input_file_name", help="input file(s)")

parser.add_argument("variable_name", help="input variable name")

parser.add_argument("output_file_name", help="output file name")

parser.add_argument("--lon_name", help="longitude name", default='lon')

parser.add_argument("--lat_name", help="latitude name", default='lat')

parser.add_argument("--time_name", help="time name", default='time')

parser.add_argument("--extent", nargs='+', type=float, help="spatial selection as South North West East")

def valid_datetime_type(arg_datetime_str):
    """custom argparse type for user datetime values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-MM-DD HH:mm'!".format(arg_datetime_str)
    raise argparse.ArgumentTypeError(msg)
    
parser.add_argument('--startdate', type=valid_datetime_type,help='start datetime in format "YYYY-MM-DD HH:mm"')

parser.add_argument('--enddate', type=valid_datetime_type,help='end datetime in format "YYYY-MM-DD HH:mm"')

# parser.add_argument("--period", type=list, help="temporal selection")

parser.add_argument("--time_unit", help="speficy time unit in dataset")

parser.add_argument("--calendar", help="specify calendar type in dataset")

args = parser.parse_args()

args.period = [args.startdate, args.enddate]

dataset = load_data(str(args.input_file_name), lon_name=args.lon_name, lat_name=args.lat_name, time_name=args.time_name,
                    extent=args.extent, period=args.period)

l_tim_mean = False
l_spa_mean = False
l_tim_median = False
l_spa_median = False
l_tim_var = False
l_spa_var = False
l_tim_std = False
l_spa_std = False
l_tim_min = False
l_spa_min = False
l_tim_max = False
l_spa_max = False

if args.stat_function == 'tim_mean':
    l_tim_mean = True
if args.stat_function == 'spa_mean':
    l_spa_mean = True
if args.stat_function == 'tim_median':
    l_tim_median = True
if args.stat_function == 'spa_median':
    l_spa_median = True
if args.stat_function == 'tim_var':
    l_tim_var = True
if args.stat_function == 'spa_var':
    l_spa_var = True
if args.stat_function == 'tim_std':
    l_tim_std = True
if args.stat_function == 'spa_std':
    l_spa_std = True
if args.stat_function == 'tim_min':
    l_tim_min = True
if args.stat_function == 'spa_min':
    l_spa_min = True
if args.stat_function == 'tim_max':
    l_tim_max = True
if args.stat_function == 'spa_max':
    l_spa_max = True

# TEMPORAL MEAN
if l_tim_mean:
    with ProgressBar():
        var_stat = dataset[args.variable_name].mean(dim=args.time_name, skipna=True).transpose(
            args.lat_name, args.lon_name).compute()
        var_stat.attrs['long_name'] = 'Temporal mean of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# SPATIAL MEAN
if l_spa_mean:
    with ProgressBar():
        var_stat = dataset[args.variable_name].mean(dim=(args.lon_name, args.lat_name), skipna=True).compute()
        var_stat.attrs['long_name'] = 'Spatial mean of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# TEMPORAL MEDIAN
if l_tim_median:
    with ProgressBar():
        var_stat = dataset[args.variable_name].median(dim=args.time_name, skipna=True).transpose(
            args.lat_name, args.lon_name).compute()
        var_stat.attrs['long_name'] = 'Temporal median of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# SPATIAL MEDIAN
if l_spa_median:
    with ProgressBar():
        var_stat = dataset[args.variable_name].median(
            dim=(args.lon_name, args.lat_name), skipna=True).compute()
        var_stat.attrs['long_name'] = 'Spatial median of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# TEMPORAL VARIANCE
if l_tim_var:
    with ProgressBar():
        var_stat = dataset[args.variable_name].var(dim=args.time_name, skipna=True).transpose(
            args.lat_name, args.lon_name).compute()
        var_stat.attrs['long_name'] = 'Temporal variance of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# SPATIAL VARIANCE
if l_spa_var:
    with ProgressBar():
        var_stat = dataset[args.variable_name].var(
            dim=(args.lon_name, args.lat_name), skipna=True).compute()
        var_stat.attrs['long_name'] = 'Spatial variance of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# TEMPORAL STD
if l_tim_std:
    with ProgressBar():
        var_stat = dataset[args.variable_name].std(dim=args.time_name, skipna=True).transpose(
            args.lat_name, args.lon_name).compute()
        var_stat.attrs['long_name'] = 'Temporal standard deviation of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# SPATIAL STD
if l_spa_std:
    with ProgressBar():
        var_stat = dataset[args.variable_name].std(dim=(args.lon_name, args.lat_name), skipna=True).compute()
        var_stat.attrs['long_name'] = 'Spatial standard deviation of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# TEMPORAL MIN
if l_tim_min:
    with ProgressBar():
        var_stat = dataset[args.variable_name].min(dim=args.time_name, skipna=True).transpose(
            args.lat_name, args.lon_name).compute()
        var_stat.attrs['long_name'] = 'Temporal minimum of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# SPATIAL MIN
if l_spa_min:
    with ProgressBar():
        var_stat = dataset[args.variable_name].min(dim=(args.lon_name, args.lat_name), skipna=True).compute()
        var_stat.attrs['long_name'] = 'Spatial minimum of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# TEMPORAL MAX
if l_tim_max:
    with ProgressBar():
        var_stat = dataset[args.variable_name].max(dim=args.time_name, skipna=True).transpose(
            args.lat_name, args.lon_name).compute()
        var_stat.attrs['long_name'] = 'Temporal maximum of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# SPATIAL MAX
if l_spa_max:
    with ProgressBar():
        var_stat = dataset[args.variable_name].max(dim=(args.lon_name, args.lat_name), skipna=True).compute()
        var_stat.attrs['long_name'] = 'Spatial maximum of variable %s in file %s' % (
            args.variable_name, args.input_file_name)
        var_stat.to_netcdf(path=args.output_file_name, mode='w', format='NETCDF4')

# DISPLAY
# if display:
#    var_stat.plot()
#     plt.show()

print('Output file saved as : %s' % args.output_file_name)
