#! /usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

url = "http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv&cql_filter=origintime>='2011-01-01T00:00:00.000Z'+AND+depth<50+AND+WITHIN(origin_geom,POLYGON((175.5957+-39.1695,+175.6478+-39.0827,+175.7036+-39.1121,+175.6619+-39.1833,+175.5957+-39.1695)))+AND+depth<20"
cat = pd.read_csv(url, parse_dates=['origintime'])

#sort by origintime, so events in time order
cat.sort_values(['origintime'], ascending=True, inplace=True)
cat = cat.reset_index()

fig = plt.figure(figsize=(15, 15))

#magnitude vs time
ax1 = fig.add_subplot(3, 1, 1)
#automatic locations
time = pd.to_datetime(cat.origintime[cat['evaluationmode']=='automatic'])
automatic = cat.magnitude[cat['evaluationmode']=='automatic']
ax1.plot(time, automatic, marker='o', color='red', linestyle='None', label='automatic')
#ax1.bar(time, automatic, width = 0.005, color='red', edgecolor='red', align='edge', label='automatic')
#manual locations
time = pd.to_datetime(cat.origintime[cat['evaluationmode']=='manual'])
manual = cat.magnitude[cat['evaluationmode']=='manual']
ax1.plot(time, manual, marker='o', color='blue', linestyle='None', label='manual')
#ax1.bar(time, manual, width = 0.005, color='blue', edgecolor='blue', align='edge', label='manual')
plt.ylabel('magnitude')
plt.legend()

#cumulative number
ax2 = fig.add_subplot(3, 1, 2, sharex = ax1)
ax2.plot(cat.origintime, cat.index, color='red', marker='None', label='cumnum')
ax2.tick_params(axis='y', colors='red')
ax2.set_ylabel('cumulative number', color = 'red')

#cumulative energy (normalised to 1.0), on same plot
ax2a= ax2.twinx()
cat['energy'] = pow(10,(1.44 * cat['magnitude'] + 5.24))
cat['cumeng'] = cat['energy'].cumsum()
cat['cumeng'] = cat['cumeng'] / cat['cumeng'].max()
ax2a.plot(cat.origintime, cat.cumeng, color='blue', marker='None', label='cumeng')
ax2a.tick_params(axis='y', colors='blue')
ax2a.set_ylabel('cumulative energy', color = 'blue')

#depth
ax3 = fig.add_subplot(3, 1, 3, sharex = ax1)
#automatic locations
time = pd.to_datetime(cat.origintime[cat['evaluationmode']=='automatic'])
automatic = cat.depth[cat['evaluationmode']=='automatic']
ax3.plot(time, automatic, color='red', marker='o', linestyle='None', label='automatic')
#manual locations
time = pd.to_datetime(cat.origintime[cat['evaluationmode']=='manual'])
manual = cat.depth[cat['evaluationmode']=='manual']
ax3.plot(time, manual, color='blue', marker='o', linestyle='None', label='manual')
plt.gca().invert_yaxis()
ax3.set_ylabel('depth(km)')
plt.legend()
