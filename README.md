# catevents
GeoNet earthquake catalogue event time-series plotting

The python script ```catevents.py``` generates a series of time-series plots of basic aspects of seismicity derived from a file extracted from the GeoNet earthquake catalogue.

To run ```catevents.py catevents.cfg ```

```catevents.py``` creates a url to carryout a search on the [GeoNet earthquake catalogue] (http://wfs.geonet.org.nz/)
A typical search url is similar to ```http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv&cql_filter=BBOX(origin_geom,174,-41,175,-42)+AND+origintime>='2009-08-01'+AND+magnitude>4```

The file ```catevents.cfg``` contains configuration information for ```catevents.py```.
```
[web]
server: volcano.gns.cri.nz
user: volcano
webdir: /var/www/html/seismic_time-series

[plot]
xsize: 15
ysize: 5
plot_dir: /home/sherburn/Dropbox/work/catevents

[region-tongariro_ngauruhoe]
startdate: 2010-01-01T00:00:00.0Z
maxdepth: 20
polygon: 175.595+-39.162,+175.652+-39.089,+175.702+-39.109,+175.641+-39.186,+175.595+-39.162

[region-tongariro]
startdate: 2010-01-01T00:00:00.0Z
maxdepth: 20
polygon: 175.616+-39.135,+175.652+-39.089,+175.702+-39.109,+175.663+-39.157,+175.616+-39.135
```
