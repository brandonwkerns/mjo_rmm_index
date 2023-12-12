#!/bin/sh -x

# The location of the BOM MJO data on the internet
http_file='http://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt'

# If there is a current file, save a backup.
# Otherwise, this step does nothing
# and the next one will download a fresh copy.
if [ -f ./rmm.74toRealtime.txt ]
then
    mv ./rmm.74toRealtime.txt ./rmm.74toRealtime.txt.bak
fi

if [ -f ./rmm.nc ]
then
    mv ./rmm.nc ./rmm.nc.bak
fi

# Download the latest data.
# Must use --user-agent to avoid 403 permission denied.
wget --user-agent "Mozilla"  $http_file  

# Use the Python script to convert to NetCDF.
python ./rmm2nc.py

# Check to make sure it was successful
if [ -f ./rmm.nc ]
then
    echo "Successfully updated rmm.nc."
    exit 0
else
    echo "There was a problem creating rmm.nc."
    exit 1
fi
