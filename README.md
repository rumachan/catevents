# catevents
GeoNet earthquake catalogue event time-series plotting

The python script ```catevents.py``` generates a series of time-series plots of basic aspects of seismicity derived from a file extracted from the GeoNet earthquake catalogue.

To run ```catevents.py catevents.cfg ```

```catevents.py``` creates a url to carryout a search on the [GeoNet earthquake catalogue] (http://wfs.geonet.org.nz/).
A typical search url is similar to ```http://wfs.geonet.org.nz/geonet/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonet:quake_search_v1&outputFormat=csv&cql_filter=BBOX(origin_geom,174,-41,175,-42)+AND+origintime>='2009-08-01'+AND+magnitude>4```

The file ```catevents.cfg``` contains configuration information for ```catevents.py```.
The start date for the query (and plot) can be specified in two ways, either by giving a date-time or a number of days before the current date-time.

The resulting png plot files are written to a local directory.
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
datetype: datetime
startdate: 2010-01-01T00:00:00.0Z
maxdepth: 20
polygon: 175.595+-39.162,+175.652+-39.089,+175.702+-39.109,+175.641+-39.186,+175.595+-39.162

[region-tongariro_ngauruhoe_a]
datetype: daysbefore
startdate: 365
maxdepth: 20
polygon: 175.595+-39.162,+175.652+-39.089,+175.702+-39.109,+175.641+-39.186,+175.595+-39.162
```

### Docker

To install and run the scripts in a docker image proceed as follows.

First get the source code:

```
git clone  --depth=1  https://github.com/rumachan/catevents.git
```

To build and run the docker image you can use the `buildnrun.sh` script:

```
cd catevents 
./buildnrun.sh -h
Usage: ./buildnrun.sh [Options]

Build and run docker image.

Options:
    -h              Show this message.
    -r              Only run image without rebuilding it.
    -b              Only rebuild image without running it.
    -t              Assign a tag to the docker image (default: latest).
```

By default `buildnrun.sh` runs both the build and run stage.

Using the `buildnrun.sh` script also requires the docker volume `html` to be present 
where plots are stored.

To generate it run:

```
docker volume create html
```

