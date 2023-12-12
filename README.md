# RMM Index for the MJO: Download and Plot

This repository contains Python code to Download the official Australia Bureau of Meteorology RMM Index data, convert it from text to NetCDF, and plot phase diagrams for a specified time period.

For more information on the RMM index, consult the following journal article:

Wheeler, M. C., and H. H. Hendon, 2004: An all-season real-time multivariate MJO index: Development of an index for monitoring and prediction. Mon. Wea. Rev., 132, 1917–1932, doi:10.1175/1520-0493(2004)132<1917:AARMMI>2.0.CO;2.

See also the following websites:
http://www.bom.gov.au/climate/mjo/
https://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo.shtml


## The Code

There are three Python scripts with functions that can be adopted in other scripts.

### do.update_rmm.sh

This script downloads the latest data from the BOM. It also runs the script `rmm2nc.py` to convert the data to NetCDF format.

It will save existing data in the directory to backup files.



## Example Plots

Here are three plots of the RMM Index for January - May 2023. This period of time is significant because a strong El Nino was spinning up, and MJO events are often connected to warming sea surface temperatures during the onset of El Nino:

Jauregui, Y. R., and S. S. Chen, 2023a: MJO-induced Warm Pool Eastward Extension Prior to the Onset of El Niño: Observations from 1998-2019, J. Clim, accepted. 



