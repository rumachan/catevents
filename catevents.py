#! /usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

url = 'http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&maxFeatures=2000&outputFormat=csv'
cat = pd.read_csv(url, parse_dates=[2])

#sort by origintime, so events in time order
cat.sort_values(['origintime'], ascending=True, inplace=True)
cat = cat.reset_index()

fig = plt.figure(figsize=(15, 5))

#magnitude vs time
ax1 = fig.add_subplot(2, 1, 1)
time = pd.to_datetime(cat.origintime)
ax1.bar(time, cat.magnitude, width = 0.01, color='red', edgecolor='red', align='edge')
plt.ylabel('magnitude')

#cumulative number
ax2 = fig.add_subplot(2, 1, 2, sharex = ax1)
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
