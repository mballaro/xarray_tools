import matplotlib.pyplot as plt
from dask.diagnostics import ProgressBar
from rw import load_data
import argparse
import numpy as np
from sys import exit

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

parser.add_argument("--period", type=list, help="temporal selection")

args = parser.parse_args()

dataset1 = load_data(str(args.input_file_name1), lon_name=args.lon_name1, lat_name=args.lat_name1,
                     time_name=args.time_name1, extent=args.extent, period=args.period)

dataset2 = load_data(str(args.input_file_name2), lon_name=args.lon_name2, lat_name=args.lat_name2,
                     time_name=args.time_name2, extent=args.extent, period=args.period)

# make commom time axis to avoid pb below
try:
    if dataset1[args.time_name1].size == dataset2[args.time_name2].size:
        dataset2[args.time_name2] = dataset1[args.time_name1]
    else:
        print('time variable have different size')
        exit()
except KeyError:
    pass
# Rename lon/lat variable if input have different name
if args.lon_name1 != args.lon_name2:
    dataset2 = dataset2.rename({args.lon_name2: args.lon_name1})

if args.lat_name1 != args.lat_name2:
    dataset2 = dataset2.rename({args.lat_name2: args.lat_name1})

# applt mask selection
# dataset2 = dataset2.where(np.abs(dataset2[args.variable_name2]) < 100.)

l_add = False
l_sub = False
l_mul = False
l_div = False
l_tim_rmse = False
l_tim_mae = False
l_spa_rmse = False
l_spa_mae = False

if args.arithmetic_function == 'add':
    l_add = True
if args.arithmetic_function == 'sub':
    l_sub = True
if args.arithmetic_function == 'mul':
    l_mul = True
if args.arithmetic_function == 'div':
    l_div = True
if args.arithmetic_function == 'tim_rmse':
    l_tim_rmse = True
if args.arithmetic_function == 'tim_mae':
    l_tim_mae = True
if args.arithmetic_function == 'spa_rmse':
    l_spa_rmse = True
if args.arithmetic_function == 'spa_mae':
    l_spa_mae = True

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

# TEMPORAL RMSE
if l_tim_rmse:
    with ProgressBar():
        new_dataset = np.sqrt(np.square(args.scale_factor1*dataset1[args.variable_name1] -
                                        args.scale_factor2*dataset2[args.variable_name2]).mean(
            dim=args.time_name1, skipna=True).transpose(args.lat_name1, args.lon_name1).compute())
        new_dataset.to_netcdf(path=str(args.output_file_name), mode='w', format='NETCDF4')

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

print('Output file saved as : %s' % args.output_file_name)
