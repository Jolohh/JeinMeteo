from matplotlib.axes import Axes
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mdates
import numpy as np
from math import floor, ceil

#eventuell bound statt limit benuten ?
#was wenn linspace faxen macht ?
#autostep funktion, die nach den Einheiten schaut und ganze vielfache nimmt, bei zeit dann aber vielfache von 15, 30, 60, etc.

def set_xstep(ax: Axes, step: float, keeplim: bool = True):
    left,right = ax.get_xlim()
    _left = floor(left/step)*step
    _right = ceil(right/step)*step

    ax.set_xticks(np.arange(_left,_right+step,step))
    if keeplim:
        ax.set_xlim(left,right)
    
    

    
def set_ystep(ax: Axes, step: float, keeplim: bool = True):
    bottom,top = ax.get_ylim()
    _bottom = floor(bottom/step)*step
    _top = ceil(top/step)*step

    
    ax.set_yticks(np.arange(_bottom,_top+step,step))
    if keeplim:
        ax.set_ylim(bottom,top)

    
def set_xunit(axis: Axes, unit: str):
    axis.xaxis.set_major_formatter(FormatStrFormatter(f'%g {unit}'))


def set_yunit(axis: Axes, unit: str):
    axis.yaxis.set_major_formatter(FormatStrFormatter(f'%g {unit}'))

def set_time_axis(axis: Axes,auto_range=True,min=0,max=24,step=2):
    axis.xaxis.remove_overlapping_locs = False

    axis.xaxis.set_major_locator(mdates.HourLocator(12))
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    if not auto_range:
        axis.xaxis.set_minor_locator(mdates.HourLocator(np.arange(min,max,step)))
    else:
        axis.xaxis.set_major_locator(mdates.AutoDateLocator())
        
    axis.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))

    axis.tick_params(which="minor", axis="x", labelsize=8)
    axis.tick_params(which="major", axis="x", pad=20, size=2)