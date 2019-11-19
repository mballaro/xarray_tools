import matplotlib.pyplot as plt
from dask.diagnostics import ProgressBar
from rw import load_data
import xarray as xr
import argparse
import numpy as np
from sys import exit
import datetime
from numba import jit

display = False

parser = argparse.ArgumentParser(description='Perform arimethic analysis on dataset')

parser.add_argument("arithmetic_function", help="arithmetic function to apply (add, sub, mul, div, tim_rmse, tim_mae, "
                                                "spa_rmse, spa_mae)")

parser.add_argument("input_file_name1", help="input file(s) #1")

parser.add_argument("variable_name1", help="input variable name #1")

parser.add_argument("input_file_name2", help="input file(s) # 2")

parser.add_argument("variable_name2", help="input variable name #2")

parser.add_argument("output_file_name", help="output file name")

parser.add_argument("--lon_name1", help="longitude name #1", default='lon')

parser.add_argument("--lat_name1", help="latitude name #1", default='lat')

parser.add_argument("--time_name1", help="time name #1", default='time')

parser.add_argument("--scale_factor1", type=float, help="scale factor to apply in datatset #1", default=1.0)

parser.add_argument("--time_unit1", help="specify time unit in dataset #1")

parser.add_argument("--calendar1", help="specify calendar type in dataset #1")

parser.add_argument("--lon_name2", help="longitude name #2", default='lon')

parser.add_argument("--lat_name2", help="latitude name #2", default='lat')

parser.add_argument("--time_name2", help="time name #2", default='time')

parser.add_argument("--scale_factor2", type=float, help="scale factor to apply in dataset #2", default=1.0)

parser.add_argument("--time_unit2", help="specify time unit in dataset #2")

parser.add_argument("--calendar2", help="specify calendar type in dataset #2")

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

args = parser.parse_args()

args.period = [args.startdate, args.enddate]

dataset1 = load_data(str(args.input_file_name1), lon_name=args.lon_name1, lat_name=args.lat_name1,
                     time_name=args.time_name1, extent=args.extent, period=args.period)

dataset2 = load_data(str(args.input_file_name2), lon_name=args.lon_name2, lat_name=args.lat_name2,
                     time_name=args.time_name2, extent=args.extent, period=args.period)

# make commom time axis to avoid pb below
try:
    if dataset1[args.time_name1].size == dataset2[args.time_name2].size:
        dataset2[args.time_name2] = dataset1[args.time_name1]
    else:
        print('time variable have different size', dataset1[args.time_name1].size,  dataset2[args.time_name2].size)
        exit()
except KeyError:
    pass
# Rename lon/lat variable if input have different name
if args.lon_name1 != args.lon_name2:
    dataset2 = dataset2.rename({args.lon_name2: args.lon_name1})
    
if args.lat_name1 != args.lat_name2:
    dataset2 = dataset2.rename({args.lat_name2: args.lat_name1})

# print(args.scale_factor1*dataset1[args.variable_name1], args.scale_factor2*dataset2[args.variable_name2])
# applt mask selection
# dataset2 = dataset2.where(np.abs(dataset2[args.variable_name2]) < 100.)


def covariance_gufunc(x, y):
    return ((x - x.mean(axis=-1, keepdims=True))
            * (y - y.mean(axis=-1, keepdims=True))).mean(axis=-1)

def pearson_correlation_gufunc(x, y):
    return covariance_gufunc(x, y) / (x.std(axis=-1) * y.std(axis=-1))

def pearson_correlation(x, y, dim):
    return xr.apply_ufunc(
        pearson_correlation_gufunc, x, y,
        input_core_dims=[[dim], [dim]],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float])



#def covariance(x, y, dims=None):
#    return xr.dot(x - x.mean(dims), y - y.mean(dims), dims=dims) / x.count(dims)

#def corrrelation(x, y, dims=None):
#    return covariance(x, y, dims) / (x.std(dims) * y.std(dims))
 

l_add = False
l_sub = False
l_mul = False
l_div = False
l_tim_rmse = False
l_tim_mae = False
l_tim_var = False
l_tim_skill = False
l_spa_rmse = False
l_spa_var = False
l_spa_mae = False
l_spa_corr = False
l_tim_corr = False

if args.arithmetic_function == 'add':
    l_add = True
if args.arithmetic_function == 'sub':
    l_sub = True
if args.arithmetic_function == 'mul':
    l_mul = True
if args.arithmetic_function == 'div':
    l_div = True
if args.arithmetic_function == 'tim_corr':
    l_tim_corr = True
if args.arithmetic_function == 'tim_rmse':
    l_tim_rmse = True
if args.arithmetic_function == 'tim_mae':
    l_tim_mae = True
if args.arithmetic_function == 'tim_var':
    l_tim_var = True
if args.arithmetic_function == 'tim_skill':
    l_tim_skill = True
if args.arithmetic_function == 'spa_rmse':
    l_spa_rmse = True
if args.arithmetic_function == 'spa_mae':
    l_spa_mae = True
if args.arithmetic_function == 'spa_corr':
    l_spa_corr = True
if args.arithmetic_function == 'spa_var':
    l_spa_var = True

if l_spa_corr:
	pass
else:
    # for time averaging
    dataset1 = dataset1.chunk({args.time_name1: len(dataset1.time), args.lat_name1: 100, args.lon_name1: 200})
    dataset2 = dataset2.chunk({args.time_name2: len(dataset1.time), args.lat_name1: 100, args.lon_name1: 200})


# ADD
if l_add:
    with ProgressBar():
        new_dataset = args.scale_factor1*dataset1[args.variable_name1] + \
                      args.scale_factor2*dataset2[args.variable_name2]
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# SUB
if l_sub:
    with ProgressBar():
        new_dataset = args.scale_factor1*dataset1[args.variable_name1] - \
                      args.scale_factor2*dataset2[args.variable_name2]
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# MUL
if l_mul:
    with ProgressBar():
        new_dataset = args.scale_factor1*dataset1[args.variable_name1] * \
                      args.scale_factor2*dataset2[args.variable_name2]
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# DIV
if l_div:
    with ProgressBar():
        new_dataset = args.scale_factor1*dataset1[args.variable_name2] / \
                      (args.scale_factor2*dataset2[args.variable_name2])
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# TIME CORRELATION
if l_tim_corr:
    with ProgressBar():
        # force common lon/lat
        dataset1[args.lon_name1] = dataset2[args.lon_name1]
        dataset1[args.lat_name1] = dataset2[args.lat_name1]
        new_dataset = pearson_correlation(args.scale_factor1*dataset1[args.variable_name1],
                                          args.scale_factor2*dataset2[args.variable_name2],
                                          dim=args.time_name1).compute()
        #new_dataset = corrrelation(args.scale_factor1*dataset1[args.variable_name1],
        #                           args.scale_factor2*dataset2[args.variable_name2], dims=str(args.time_name1))
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# TEMPORAL RMSE
if l_tim_rmse:
    with ProgressBar():
        new_dataset = np.sqrt(np.square(args.scale_factor1*dataset1[args.variable_name1] -
                                        args.scale_factor2*dataset2[args.variable_name2]).mean(
            dim=args.time_name1, skipna=True).transpose(args.lat_name1, args.lon_name1).compute())
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')
        
# TEMPORAL VARIANCE
if l_tim_var:
    with ProgressBar():
        new_dataset = (args.scale_factor1*dataset1[args.variable_name1] -
                                        args.scale_factor2*dataset2[args.variable_name2]).var(
            dim=args.time_name1, skipna=True).transpose(args.lat_name1, args.lon_name1).compute()
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# TEMPORAL SKILL
if l_tim_skill:
    with ProgressBar():
        var_dataset1 = (args.scale_factor1 * dataset1[args.variable_name1]).var(
            dim=args.time_name1, skipna=True).transpose(args.lat_name1, args.lon_name1).compute()
        var_dataset2 = (args.scale_factor2 * dataset2[args.variable_name2]).var(
            dim=args.time_name1, skipna=True).transpose(args.lat_name1, args.lon_name1).compute()
        # force common lon/lat
        dataset1[args.lon_name1] = dataset2[args.lon_name1]
        dataset1[args.lat_name1] = dataset2[args.lat_name1]
        corr_dataset = pearson_correlation(args.scale_factor1 * dataset1[args.variable_name1],
                                          args.scale_factor2 * dataset2[args.variable_name2],
                                          dim=args.time_name1).compute()
        new_dataset = 2.*(1.+corr_dataset) / ((var_dataset1/var_dataset2 + var_dataset2/var_dataset1)**2)
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')
        del var_dataset1
        del var_dataset2
        del corr_dataset

# TEMPORAL ABSOLUTE ERROR
if l_tim_mae:
    with ProgressBar():
        new_dataset = np.abs(args.scale_factor1*dataset1[args.variable_name1] -
                             args.scale_factor2*dataset2[args.variable_name2]).mean(
            dim=args.time_name1, skipna=True).transpose(args.lat_name1, args.lon_name1).compute()
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# SPATIAL RMSE
if l_spa_rmse:
    with ProgressBar():
        new_dataset = np.sqrt(np.square(args.scale_factor1*dataset1[args.variable_name1] -
                                        args.scale_factor2*dataset2[args.variable_name2]).mean(
            dim=(args.lon_name1, args.lat_name1), skipna=True).compute())
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# SPATIAL ABSOLUTE ERROR
if l_spa_mae:
    with ProgressBar():
        new_dataset = np.abs(args.scale_factor1*dataset1[args.variable_name1] -
                             args.scale_factor2*dataset2[args.variable_name2]).mean(
            dim=(args.lon_name1, args.lat_name1), skipna=True).compute()
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# SPATIAL VARIANCE
if l_spa_var:
    with ProgressBar():
        new_dataset = (args.scale_factor1*dataset1[args.variable_name1] -
                                        args.scale_factor2*dataset2[args.variable_name2]).var(
            dim=(args.lon_name1, args.lat_name1), skipna=True).compute()
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

# SPATIAL CORRELATION
if l_spa_corr:
    with ProgressBar():
		# force common lon/lat
        dataset2[args.lon_name1] = dataset1[args.lon_name1]
        dataset2[args.lat_name1] = dataset1[args.lat_name1]
        
        dataset = xr.merge([dataset1, dataset2])
        #del dataset1
        #del dataset2
        dataset = dataset.where((dataset[args.variable_name1] != np.nan) | (dataset[args.variable_name2] != np.nan), drop=True)
        
        # reshape
        # print(len(dataset[args.lon_name1]),dataset[args.variable_name1].stack(z=('lon', 'lat')))
        #print(dataset)
        #print('1', dataset1)
        #print('2', dataset2)
        new_dataset = pearson_correlation(args.scale_factor1*dataset[args.variable_name1].stack(z=(args.lon_name1, args.lat_name1)).dropna('z'),
                                          args.scale_factor2*dataset[args.variable_name2].stack(z=(args.lon_name1, args.lat_name1)).dropna('z'),
                                          dim=('z')).compute()
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')
     
        
print('Output file saved as : %s' % args.output_file_name)
del dataset1
del dataset2
del new_dataset
