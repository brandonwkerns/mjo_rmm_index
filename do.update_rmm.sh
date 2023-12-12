#!/bin/sh -x

http_file='http://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt'

cd /home/orca/data/indices/MJO/RMM
echo `pwd`
mv ./rmm.74toRealtime.txt ./rmm.74toRealtime.txt.bak
mv ./rmm.nc ./rmm.nc.bak

wget --user-agent "Mozilla"  $http_file  ## Must use --user-agent to avoid 403 permission denied.

source /home/disk/orca/bkerns/anaconda3/bin/activate meteo

/home/disk/orca/bkerns/anaconda3/envs/meteo/bin/python ./rmm2nc.py

exit 0


