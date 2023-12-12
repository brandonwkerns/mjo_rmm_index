# RMM Index for the MJO: Download and Plot

This repository contains Python code to Download the official Australia Bureau of Meteorology RMM Index data, convert it from text to NetCDF, and plot phase diagrams for a specified time period.

For more information on the RMM index, consult the following journal article:

Wheeler, M. C., and H. H. Hendon, 2004: An all-season real-time multivariate MJO index: Development of an index for monitoring and prediction. Mon. Wea. Rev., 132, 1917–1932, doi:10.1175/1520-0493(2004)132<1917:AARMMI>2.0.CO;2.

See also the following websites:
- http://www.bom.gov.au/climate/mjo/
- https://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo.shtml


## The Environment

The Python dependencies are: Numpy, netCDF4, matplotlib, and colorcet.
It should not be very picky about versions.

The file **requirements.txt** can be used to build a PIP virtual environment
like this:
```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## The Code

There are three Python scripts with functions that can be adopted in other scripts.

### do.update_rmm.sh

This script downloads the latest data from the BOM. It also runs the script `rmm2nc.py` to convert the data to NetCDF format.

It will save existing data in the directory to backup files.

### rmm2nc.py

This Python script converts the text file rmm.74toRealtime.txt to
the NetCDF file rmm.nc.

### plot_rmm_phase_diagram.py

This Python function and script plots a RMM Index phase diagram
for the date range specified.

Specify a beginning and ending date in YYYYMMDD format, for example:
`python plot_rmm_phase_diagram 20230419 20230530`

The plot naming convention is **rmm_20230419_to_20230530.png**.

If no date range is specified, it will print out:
**Usage: plot_rmm_phase_diagram.py YYYYMMDD_begin YYYYMMDD_end**.


## Example Plots

Here are three plots of the RMM Index for January - May 2023. This period of time is significant because a strong El Nino was spinning up, and MJO events are often connected to warming sea surface temperatures during the onset of El Nino:

Jauregui, Y. R., and S. S. Chen, 2023a: MJO-induced Warm Pool Eastward Extension Prior to the Onset of El Niño: Observations from 1998-2019, J. Clim, accepted. 

The plots were generated using these commands:
```
do.update_rmm.sh
python plot_rmm_phase_diagram.py 20230118 20230223
python plot_rmm_phase_diagram.py 20230226 20230405
python plot_rmm_phase_diagram.py 20230419 20230530
```

![rmm_20230118_to_20230223](https://github.com/brandonwkerns/mjo_rmm_index/assets/18037033/18eafe6f-5e64-45ab-86b4-58474d73e4d8)
![rmm_20230226_to_20230405](https://github.com/brandonwkerns/mjo_rmm_index/assets/18037033/411b4d57-1dbf-4a0a-bbbb-8a511650ff6a)
![rmm_20230419_to_20230530](https://github.com/brandonwkerns/mjo_rmm_index/assets/18037033/579cc581-07f9-4c26-8580-6c27b7dc9ac9)



