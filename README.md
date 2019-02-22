
`xarray_tools` performs statistical and arithmetic operations on datasets

# Table of contents
<!--ts-->
   * [Table of contents](#table-of-contents)
   * [Usage and Background](#usage-and-background "Usage and Background")
   * [First step with xarray_tools](#first-step-with-xarray_tools "First step with xarray_tools")
      * [Running test cases](#running-test-cases "Running test cases")

# Usage and Background
* `xr_stat_dataset.py` performs statistical operation of dataset
---
     >> python xr_stat_dataset.py -h 
     usage: xr_stat_dataset.py [-h] [--lon_name LON_NAME] [--lat_name LAT_NAME]
                          [--time_name TIME_NAME]
                          [--extent EXTENT [EXTENT ...]] [--period PERIOD]
                          [--time_unit TIME_UNIT] [--calendar CALENDAR]
                          stat_function input_file_name variable_name
                          output_file_name

     Performs statistcal analysis on dataset

     positional arguments:
       stat_function         statistical function to apply (tim_mean, spa_mean,
                             tim_median, spa_median, tim_var, spa_var, tim_std,
                             spa_std, tim_min, spa_min, tim_max, spa_max)
       input_file_name       input file(s)
       variable_name         input variable name
       output_file_name      output file name

     optional arguments:
       -h, --help            show this help message and exit
       --lon_name LON_NAME   longitude name
       --lat_name LAT_NAME   latitude name
       --time_name TIME_NAME time name
       --extent EXTENT [EXTENT ...] spatial selection as South North West East
       --period PERIOD       temporal selection
       --time_unit TIME_UNIT speficy time unit in dataset
       --calendar CALENDAR   specify calendar type in dataset


* `xr_combine_dataset.py` performs arithmetic operation between two datasets
---
     >> python xr_combine_dataset.py -h
     usage: xr_combine_dataset.py [-h] [--lon_name1 LON_NAME1]
                             [--lat_name1 LAT_NAME1] [--time_name1 TIME_NAME1]
                             [--scale_factor1 SCALE_FACTOR1]
                             [--time_unit1 TIME_UNIT1] [--calendar1 CALENDAR1]
                             [--lon_name2 LON_NAME2] [--lat_name2 LAT_NAME2]
                             [--time_name2 TIME_NAME2]
                             [--scale_factor2 SCALE_FACTOR2]
                             [--time_unit2 TIME_UNIT2] [--calendar2 CALENDAR2]
                             [--extent EXTENT [EXTENT ...]] [--period PERIOD]
                             arithmetic_function input_file_name1
                             variable_name1 input_file_name2 variable_name2
                             output_file_name

     Perform arimethic analysis on dataset

     positional arguments:
       arithmetic_function   arithmetic function to apply (add, sub, mul, div)
       input_file_name1      input file(s) #1
       variable_name1        input variable name #1
       input_file_name2      input file(s) # 2
       variable_name2        input variable name #2
       output_file_name      output file name

     optional arguments:
       -h, --help            show this help message and exit
       --lon_name1 LON_NAME1 longitude name #1
       --lat_name1 LAT_NAME1 latitude name #1
       --time_name1 TIME_NAME1 time name #1
       --scale_factor1 SCALE_FACTOR1 scale factor to apply in datatset #1
       --time_unit1 TIME_UNIT1 specify time unit in dataset #1
       --calendar1 CALENDAR1 specify calendar type in dataset #1
       --lon_name2 LON_NAME2 longitude name #2
       --lat_name2 LAT_NAME2 latitude name #2
       --time_name2 TIME_NAME2 time name #2
       --scale_factor2 SCALE_FACTOR2 scale factor to apply in dataset #2
       --time_unit2 TIME_UNIT2 specify time unit in dataset #2
       --calendar2 CALENDAR2 specify calendar type in dataset #2
       --extent EXTENT [EXTENT ...] spatial selection as South North West East
       --period PERIOD       temporal selection

# First step with xarray_tools
## Running test cases
---
     >> cd test_case/
     >> ./run.x


