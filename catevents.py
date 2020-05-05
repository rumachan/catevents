#! /usr/bin/env python

import pandas as pd
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
import configparser
import datetime

# input argument - configuration file
if (len(sys.argv) != 2):
    sys.exit("syntax catevents.py config_file")
else:
    cfg = sys.argv[1]

# parse configuration file
config = configparser.ConfigParser()
config.read(cfg)
server = config.get('web', 'server')
user = config.get('web', 'user')
webdir = config.get('web', 'webdir')
xsize = float(config.get('plot', 'xsize'))
ysize = float(config.get('plot', 'ysize'))
plot_dir = config.get('plot', 'plot_dir')

# get region names
regions = []
for section in config.sections():
    if 'region-' in section:
        reg = section.split('-')[1]
        regions.append(reg)

# loop through regions
for reg in regions:
    print ('region = ', reg)
    datetype = config.get('region-' + reg, 'datetype')
    startdate = config.get('region-' + reg, 'startdate')
    maxdepth = config.get('region-' + reg, 'maxdepth')
    polygon = config.get('region-' + reg, 'polygon')

    # start and now for x-axis
    # calculate startdate from days before, and namestart for plot name
    now = datetime.datetime.now()
    if (datetype == 'daysbefore'):
        namestart = startdate
        sdt = datetime.datetime.now() - datetime.timedelta(days=int(startdate))
        startdate = sdt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        start = sdt
        # print start
    if (datetype == 'datetime'):
        start = datetime.datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%S.%fZ")
        # print start
        namestart = start.strftime("%Y-%m-%d")
    titlestart = start.strftime("%Y-%m-%d %H:%M")

    url = "http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv&cql_filter=origintime>=" + \
        startdate + \
        "+AND+WITHIN(origin_geom,POLYGON((" + polygon + "+)))+AND+depth<" + \
        maxdepth
#  print url

    cat = pd.read_csv(url, parse_dates=['origintime'])

    # sort by origintime, so events in time order
    cat.sort_values(['origintime'], ascending=True, inplace=True)
    cat = cat.reset_index()

    fig = plt.figure(figsize=(15, 15))

    # magnitude vs time
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.set_xlim([start, now])
    ymax = 1.1 * cat.magnitude.max()
    ax1.set_ylim([0, ymax])
    # title
    # drop underscore_letter from end, if present
    if (reg[-2] == '_'):
        reg = reg[:-2]
    title = (reg.replace('_', ' ').title() + ', ' +
             titlestart + ' to ' + now.strftime("%Y-%m-%d %H:%M"))
    plt.title(title)
    # automatic locations
    time = pd.to_datetime(cat.origintime[cat['evaluationmode'] == 'automatic'])
    automatic = cat.magnitude[cat['evaluationmode'] == 'automatic']
    ax1.plot(time, automatic, marker='o', color='red',
             linestyle='None', label='automatic')
    #ax1.bar(time, automatic, width = 0.005, color='red', edgecolor='red', align='edge', label='automatic')
    # manual locations
    time = pd.to_datetime(cat.origintime[cat['evaluationmode'] == 'manual'])
    manual = cat.magnitude[cat['evaluationmode'] == 'manual']
    ax1.plot(time, manual, marker='o', color='blue',
             linestyle='None', label='manual')
    #ax1.bar(time, manual, width = 0.005, color='blue', edgecolor='blue', align='edge', label='manual')
    plt.ylabel('magnitude')
    plt.legend(loc='best')

    # cumulative number
    ax2 = fig.add_subplot(3, 1, 2, sharex=ax1)
    ax2.set_xlim([start, now])
    ax2.plot(cat.origintime, cat.index, color='red',
             marker='None', label='cumnum')
    ax2.tick_params(axis='y', colors='red')
    ax2.set_ylabel('cumulative number', color='red')

    # cumulative energy (normalised to 1.0), on same plot
    ax2a = ax2.twinx()
    ax2a.set_xlim([start, now])
    ax2a.set_ylim([0, 1])
    cat['energy'] = pow(10, (1.44 * cat['magnitude'] + 5.24))
    cat['cumeng'] = cat['energy'].cumsum()
    cat['cumeng'] = cat['cumeng'] / cat['cumeng'].max()
    ax2a.plot(cat.origintime, cat.cumeng, color='blue',
              marker='None', label='cumeng')
    ax2a.tick_params(axis='y', colors='blue')
    ax2a.set_ylabel('cumulative energy', color='blue')

    # depth
    ax3 = fig.add_subplot(3, 1, 3, sharex=ax1)
    ax3.set_xlim([start, now])
    ax3.set_ylim([0, float(maxdepth)])
    # automatic locations
    time = pd.to_datetime(cat.origintime[cat['evaluationmode'] == 'automatic'])
    automatic = cat.depth[cat['evaluationmode'] == 'automatic']
    ax3.plot(time, automatic, color='red', marker='o',
             linestyle='None', label='automatic')
    # manual locations
    time = pd.to_datetime(cat.origintime[cat['evaluationmode'] == 'manual'])
    manual = cat.depth[cat['evaluationmode'] == 'manual']
    ax3.plot(time, manual, color='blue', marker='o',
             linestyle='None', label='manual')
    plt.gca().invert_yaxis()
    ax3.set_ylabel('depth(km)')
    plt.legend(loc='best')

    image = os.path.join(plot_dir, reg + '_' + namestart + '.png')
    plt.savefig(image, dpi=200)
