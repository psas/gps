#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import pi, radians, degrees
import ephem
import datetime

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


print "#SV, Doppler (Hz), Alt (deg), Az (deg)"

sats = {'az': [], 'alt': [], 'color': []}
def sat(ax, SV, az, alt, dop, sats):
    dop = (dop/2.99792e8)*1.57542e9

    print ', '.join([SV, "%5.0f"%dop, "%4.1f" % degrees(alt), "%5.1f" % degrees(az)])

    az = az + pi
    alt = degrees((pi/2.0) - alt)

    sats['az'].append(az)
    sats['alt'].append(alt)
    if alt > 70:
        sats['color'].append('#ffaa00')
    else:
        sats['color'].append('#ccff33')


    #plt.plot([az, az+0.5], [alt, alt+3], c="black")
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


location = ephem.Observer()
location.lat = "45.0"
location.long = "-122.0"
location.elevation = 50
now = datetime.datetime.utcnow()
location.date = now

with open('gps-ops.txt', 'r') as datafile:

    while True:
        try:
            gps = ephem.readtle(datafile.readline(), datafile.readline(), datafile.readline())
        except:
            break

        gps.compute(location)
        if (gps.alt*1) > radians(5):
            name = gps.name.split('PRN')[1].replace(')', '').strip()
            
            sats = sat(ax, name, gps.az*1, gps.alt*1, gps.range_velocity, sats)

# plot sat dots
plt.scatter(sats['az'], sats['alt'], s=120, c=sats['color'], alpha=0.8)

# ticks
plt.xticks([0, pi/2.0, pi, 3*pi/2.0], ['W','N','E','S'])
plt.yticks([0, 45, 70], ['z',u"45°",u"20°"])
ax.set_ylim([0, 90])

# save
plt.savefig('constellation.png', dpi=120)
