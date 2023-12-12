import numpy as np
import xarray as xr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import patheffects
import matplotlib #.colormaps
from netCDF4 import Dataset
import matplotlib.colors as colors
import colorcet as ccet
import sys


def extract_rmm_for_time_period(dt_start, dt_end,
                                fn='/home/orca/data/indices/MJO/RMM/rmm.nc'):

    """extract_rmm_for_time_period

    Get the daily official RMM index for a range of dates.
    """

    with Dataset('/home/orca/data/indices/MJO/RMM/rmm.nc') as RMMDS:
        RMM = {}
        RMM['datetime'] = [dt.datetime(1970,1,1,0,0,0) + dt.timedelta(hours=int(x)) for x in RMMDS['time'][:]]
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
    """set_up_rmm_phase_diagram_axes
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


def add_rmm_index_trace(RMM, axrmm=None, cmap='viridis', add_colorbar=True):
    """add_rmm_index_trace
    usage: H = add_rmm_index_trace(RMM, axrmm=None)

    Input:
      - RMM: a dict with keys: RMM1, RMM2, datetime

    Output:
      - H: The plot object output from Scatter()
    """

    rmm1keep = RMM['RMM1']
    rmm2keep = RMM['RMM2']

    axrmm.plot(rmm1keep, rmm2keep, 'k-', linewidth=0.7)

    H = axrmm.scatter(rmm1keep,rmm2keep, s=50, marker='o',
                      c=np.linspace(0.0, 1.0, len(rmm1keep)),
                      cmap=cmap,
                      edgecolors='k')

    # Colorbar
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

    if len(sys.argv) < 2:
        print('Usage: '+sys.argv[0]+' YYYYMMDD_begin YYYYMMDD_end')

    else:
        YMD1 = sys.argv[1]
        YMD2 = sys.argv[2]
        FMT = '%Y%m%d'

        dt1 = dt.datetime.strptime(YMD1, FMT)
        dt2 = dt.datetime.strptime(YMD2, FMT)

        RMM = extract_rmm_for_time_period(dt1,dt2)
        fig = plt.figure(figsize=(4,4))
        axrmm = set_up_rmm_phase_diagram_axes(fig)

        cmap = matplotlib.colormaps['cet_rainbow4']
        H = add_rmm_index_trace(RMM, axrmm, cmap=cmap, add_colorbar=True)

        ## Title
        axrmm.text(-3.8,4.2,f'RMM Index: {YMD1} to {YMD2}',color='k',fontsize=10,fontweight='bold')

        plt.savefig(f'rmm_{YMD1}_to_{YMD2}.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
