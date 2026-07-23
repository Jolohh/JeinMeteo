from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from matplotlib.ticker import FormatStrFormatter

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

    
def set_xunit(unit):
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter(f'%d {unit}'))


def set_yunit(unit):
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter(f'%d {unit}'))
    