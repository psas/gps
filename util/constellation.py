#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import pi

mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['lines.linestyle'] = ':'
mpl.rcParams['grid.color'] ='black'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5
mpl.rcParams['grid.alpha'] = 0.3
mpl.rcParams['xtick.color'] = '#003366'
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['xtick.major.pad'] = 490
mpl.rcParams['ytick.color'] = '#9999aa'
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['patch.linewidth'] = 0.3
mpl.rcParams['patch.edgecolor'] = '#ffcc33'
mpl.rcParams['font.size'] = 4.3


sats = {'az': [], 'alt': []}
def sat(SV, ax, sats):

    alt = 23
    az = 1
    dop = -3421

    sats['az'].append(az)
    sats['alt'].append(alt)

    plt.plot([az, az+0.5], [alt, alt+3], c="black")
    ax.annotate(SV, xy=(az, alt),
        xytext=(0, -0.5), textcoords='offset points', horizontalalignment='center', verticalalignment='center',
        fontsize=6
    )
    ax.annotate("%0.0f Hz" % dop, xy=(az, alt), 
        xytext=(7, 1), textcoords='offset points', horizontalalignment='left', verticalalignment='center',
        color='#555555'
    )
    return sats


# make figure
fig, ax = plt.subplots(1, 1, subplot_kw=dict(polar=True))

# append sats
sats = sat('8', ax, sats)

# plot sat dots
plt.scatter(sats['az'], sats['alt'], s=120, c='#ccff22', alpha=0.8)

# ticks
plt.xticks([0, pi/2.0, pi, 3*pi/2.0], ['W','N','E','S'])
plt.yticks([0, 45, 70], ['z',u"45°",u"20°"])
ax.set_ylim([0, 90])

# save
plt.savefig('test.png', dpi=120)
plt.show()
