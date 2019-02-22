#!/bin/bash

. /home/mballarotta/.virtualenvs/xarray/bin/activate

inputs="/data/PVA/v2018/Interne/ftp/CMEMS/global/dt-grids/all-sat-merged/phy/2015/dt_global_allsat_phy_l4*.nc"

variable_name='sla'

for stat_function in tim_mean spa_mean tim_median spa_median tim_var spa_var tim_std spa_std tim_min spa_min tim_max spa_max; do

    output_filename=${stat_function}.nc

    python ../xr_stat_dataset.py ${stat_function} "${inputs}" ${variable_name} ${output_filename} --lon_name longitude --lat_name latitude

done
