import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset
import colorcet as ccet # Give Matplotlib access to Colorcet colormaps.
import sys


def extract_rmm_for_time_period(dt_start, dt_end, fn='./rmm.nc'):

    """Extract RMM data for a time period.

    Get the daily official RMM index for a range of dates.
    The date range is inclusive.

    Inputs:
    - dt_start: starting date (Python datetime)
    - dt_end: ending date (Python datetime)
    - fn (optional, default ./rmm.nc): NetCDF file containing the RMM data.

    Output:
    - RMM: a dictionary with the RMM values and the datetime.
    """

    with Dataset('/home/orca/data/indices/MJO/RMM/rmm.nc') as RMMDS:
        RMM = {}
        RMM['datetime'] = [(dt.datetime(1970,1,1,0,0,0)
                            + dt.timedelta(hours=int(x))
                            ) for x in RMMDS['time'][:]]
        RMM['RMM1'] = RMMDS['rmm1'][:]
        RMM['RMM2'] = RMMDS['rmm2'][:]

    keep_idx = [x for x in range(len(RMM['datetime']))
        if (RMM['datetime'][x] > dt1 and RMM['datetime'][x] <= dt2)]
    RMM['RMM1'] = RMM['RMM1'][keep_idx]
    RMM['RMM2'] = RMM['RMM2'][keep_idx]
    RMM['datetime'] = RMM['datetime'][keep_idx[0]:keep_idx[-1]+1]

    return RMM


def set_up_rmm_phase_diagram_axes(fig,
                                  draw_axes_tick_labels=True,
                                  draw_axes_titles=True,
                                  draw_rmm_phase_labels=True):
    """Set up axes for the RMM phase diagram.

    Usage: axrmm = set_up_rmm_phase_diagram_axes(fig)
    
    Input:
    - fig: a Matplotlib figure object.
    
    Output:
    - axrmm: A Matplotlib axis object
    """
    
    axrmm = fig.add_subplot(1,1,1)
    X_rmm_1 = np.cos(np.arange(0,361,1)*np.pi/180.0)
    Y_rmm_1 = np.sin(np.arange(0,361,1)*np.pi/180.0)
    axrmm.plot(X_rmm_1,Y_rmm_1,'k',linewidth=1)

    axrmm.plot([-4.0,-1.0],[0.0,0.0],'k',linewidth=1)
    axrmm.plot([1.0,4.0],[0.0,0.0],'k',linewidth=1)

    axrmm.plot([0,0],[-4.0,-1.0],'k',linewidth=1)
    axrmm.plot([0,0],[1.0,4.0],'k',linewidth=1)

    axrmm.plot([-4.0,-0.707],[-4.0,-0.707],'k',linewidth=1)
    axrmm.plot([0.707, 4.0],[0.707, 4.0],'k',linewidth=1)

    axrmm.plot([-4.0,-0.707],[4.0,0.707],'k',linewidth=1)
    axrmm.plot([0.707, 4.0],[-0.707, -4.0],'k',linewidth=1)

    if draw_axes_tick_labels:
        axrmm.set_xlim([-4,4])
        axrmm.set_ylim([-4,4])
        axrmm.set_xticks([-4,-2,0,2,4])
        axrmm.set_yticks([-4,-2,0,2,4])

    if draw_axes_titles:
        axrmm.set_xlabel('RMM1')
        axrmm.set_ylabel('RMM2')

    if draw_rmm_phase_labels:
        axrmm.text(-3.8,2.0,'8',color='b',fontsize=10,fontweight='bold')
        axrmm.text(-3.8,-2.0,'1',color='b',fontsize=10,fontweight='bold')
        axrmm.text(-2.0,-3.8,'2',color='b',fontsize=10,fontweight='bold')
        axrmm.text(2.0,-3.8,'3',color='b',fontsize=10,fontweight='bold')
        axrmm.text(3.5,-2.0,'4',color='b',fontsize=10,fontweight='bold')
        axrmm.text(3.5,2.0,'5',color='b',fontsize=10,fontweight='bold')
        axrmm.text(2.0,3.5,'6',color='b',fontsize=10,fontweight='bold')
        axrmm.text(-2.0,3.5,'7',color='b',fontsize=10,fontweight='bold')

    axrmm.set_aspect(1.0)

    return axrmm


def add_rmm_index_trace(RMM, axrmm=None, marker='o',
                        cmap='viridis', add_colorbar=True):
    """Adds an RMM trace to the RMM phase diagram axes.

    Usage: H = add_rmm_index_trace(RMM, axrmm=None, marker='o',
                                   cmap='viridis', add_colorbar=True)

    Colors are based on the date.

    The marker and colors used to shade the markers can be specified.
    
    Input:
      - RMM: a dict with keys: RMM1, RMM2, datetime
      - axrmm: The axes object. If not specified, use plt.gca().
      - marker (default: 'o'): Marker shape to use.
      - cmap (default: 'viridis'): the colormap for daily markers.
      - add_colorbar (default: True): Whether to draw a colorbar.

    Output:
      - H: The plot object output from Scatter()
    """

    rmm1keep = RMM['RMM1']
    rmm2keep = RMM['RMM2']

    axrmm.plot(rmm1keep, rmm2keep, 'k-', linewidth=0.7)

    H = axrmm.scatter(rmm1keep,rmm2keep, s=50, marker=marker,
                      c=np.linspace(0.0, 1.0, len(rmm1keep)),
                      cmap=cmap,
                      edgecolors='k')

    # Colorbar, if specified.
    if add_colorbar:
        cax = fig.add_axes([1.0, 0.2, 0.03, 0.6])
        cbar = plt.colorbar(H, cax=cax)
        ticks = [0.0, 0.25, 0.5, 0.75, 1.0]
        FMT = '%m/%d'
        dt11 = dt1 + dt.timedelta(seconds=0.25*(dt2-dt1).total_seconds())
        dt12 = dt1 + dt.timedelta(seconds=0.5*(dt2-dt1).total_seconds())
        dt13 = dt1 + dt.timedelta(seconds=0.75*(dt2-dt1).total_seconds())
        tick_labels = [x.strftime(FMT) for x in [dt1, dt11, dt12, dt13, dt2]]
        cbar.ax.set_yticks(ticks)
        cbar.ax.set_yticklabels(tick_labels)

    return H


if __name__ == '__main__':

    # Here is a script illustrating how the above functions can be used.
    # To use it, specify the starting and ending dates on the command line
    # For example: python plot_rmm_phase_diagram.py 20230419 20230530

    if len(sys.argv) < 2:
        print('Usage: '+sys.argv[0]+' YYYYMMDD_begin YYYYMMDD_end')

    else:
        YMD1 = sys.argv[1]
        YMD2 = sys.argv[2]
        FMT = '%Y%m%d'

        # Get datetime from date strings
        dt1 = dt.datetime.strptime(YMD1, FMT)
        dt2 = dt.datetime.strptime(YMD2, FMT)

        # Extract the data for the time period
        RMM = extract_rmm_for_time_period(dt1,dt2)

        # Set up the figure and RMM phase diagram axes
        fig = plt.figure(figsize=(4,4))
        axrmm = set_up_rmm_phase_diagram_axes(fig)

        # Draw the RMM index trace on the phase diagram
        cmap = matplotlib.colormaps['cet_rainbow4']
        H = add_rmm_index_trace(RMM, axrmm, cmap=cmap, add_colorbar=True)

        ## Add a title
        axrmm.text(-3.8,4.2,f'RMM Index: {YMD1} to {YMD2}',color='k',
                   fontsize=10,fontweight='bold')

        ## Save the output to a png file
        fnout = f'rmm_{YMD1}_to_{YMD2}.png'
        print(f'--> {fnout}')
        plt.savefig(fnout, dpi=100, bbox_inches='tight')
        plt.close(fig)
