#! /usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import ConfigParser
import datetime
from subprocess import call

#input argument - configuration file
if (len(sys.argv) != 2):
  sys.exit("syntax cateevents.py config_file")
else:
  cfg = sys.argv[1]

#parse configuration file
config = ConfigParser.ConfigParser()
config.read(cfg)
server = config.get('web','server')
user = config.get('web','user')
webdir = config.get('web','webdir')
xsize = float(config.get('plot','xsize'))
ysize = float(config.get('plot','ysize'))
plot_dir = config.get('plot','plot_dir')


#get region names
regions = []
for section in config.sections():
  if 'region-' in section:
    reg = section.split('-')[1]
    regions.append(reg)

#loop through regions
for reg in regions:
  print 'region = ', reg
  startdate = config.get('region-'+reg,'startdate')
  maxdepth = config.get('region-'+reg,'maxdepth')
  polygon = config.get('region-'+reg,'polygon')
  #print startdate
  #print maxdepth
  #print polygon

  url = "http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv&cql_filter=origintime>="+startdate+"+AND+WITHIN(origin_geom,POLYGON(("+polygon+"+)))+AND+depth<"+maxdepth
  #print url

  cat = pd.read_csv(url, parse_dates=['origintime'])

  #sort by origintime, so events in time order
  cat.sort_values(['origintime'], ascending=True, inplace=True)
  cat = cat.reset_index()

  fig = plt.figure(figsize=(15, 15))

  #title
  now = datetime.datetime.now()
  title = (reg.capitalize()+ ', plotted at: '+ now.strftime("%Y-%m-%d %H:%M"))
  plt.title(title)

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

  image = os.path.join(plot_dir, reg+'.png')
  plt.savefig(image, dpi=200)

  #send image to web server
  cmdstr = '/usr/bin/scp '+ image + ' ' +user +'@' + server + ':' + webdir
  #call(cmdstr, shell=True)
