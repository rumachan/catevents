# catevents
GeoNet earthquake catalogue event time-series plotting

The python script ```catevents.py``` generates a series of time-series plots of basic aspects of seismicity derived from a file extracted from the GeoNet earthquake catalogue.

To run ```catevents.py catevents.cfg ```

```catevents.py``` creates a url to carryout a search on the [GeoNet earthquake catalogue] (http://wfs.geonet.org.nz/)

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
