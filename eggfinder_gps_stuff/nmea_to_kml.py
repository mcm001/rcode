from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
import datetime

import pynmea2
stri = ""

# f = open("latlong.csv", 'w')

# launchTime = datetime.datetime(2021,9,19,18,58,32)
launchTime = datetime.datetime(2021,9,19,18,58,20 + 5, 670000)

dat = []
latlng = []

import numpy as np
import matplotlib.pyplot as plt

# for line in open("D:\\Documents\\machiavelli combined gps.log"):
for line in open("D:\\Documents\\machiavelli.txt"):
    # print(line)
    try:
        p = pynmea2.parse(line)
        # stri += (f"{p.longitude},{p.latitude},{10} ")
        if p.longitude != 0 and p.latitude != 0:
            # f.write(f"{p.longitude},{p.latitude}\n")
            
            time = datetime.datetime(2021,9,19, p.timestamp.hour, p.timestamp.minute, p.timestamp.second)
            dt = (time-launchTime).total_seconds()

            dat.append([dt, p.altitude])
            latlng.append([dt, p.latitude, p.longitude])


            # print(p.spd_over_grnd)
            # print(p.altitude)
    except Exception as e:
        print(e)
        pass

altData = [line.strip().split(",") for line in open("D:\\Documents\\Machiavelli Strat 3 9-19-21.csv")]
altData = np.array(altData)[:,0:2]
altData = altData.astype(np.float)
altData = altData[20:,:]

dat = np.array(dat)
dat = dat[759:,:]
latlng=np.array(latlng)
latlng = latlng[759:,:]

plt.figure()
plt.subplot(221)
plt.title("GPS altitude over time plus T0")
plt.plot(dat[:,0], dat[:,1])
plt.xlim(0,50)
plt.subplot(223)
plt.title("Strat altitude over time plus T0")
plt.plot(altData[:,0], altData[:,1])
plt.xlim(0,50)
plt.subplot(222)
plt.title("Lat vs time")
plt.plot(latlng[:,0], latlng[:,1])
plt.subplot(224)
plt.title("Lng vs time")
plt.plot(latlng[:,0], latlng[:,2])
plt.show()

# f.close()


doc = KML.kml(
    KML.Placemark(
        KML.name("gx:altitudeMode Example"),
        KML.LookAt(
            KML.longitude(-73.16),
            KML.latitude(44.8),
            KML.heading(0),
            KML.tilt(70),
            KML.range(100),
            GX.altitudeMode("relativeToGround"),
        ),
        KML.LineString(
            # KML.extrude(1),
            GX.altitudeMode("absolute"),
            KML.coordinates(
                # array
                # stri,
            #   "146.825,12.233,12000 "
            #   "146.820,12.222,400 "
            #   "146.812,12.212,400 "
            #   "146.796,12.209,400 "
            #   "146.788,12.205,400"
              "-73.16462,44.824807,55.8 -73.164625,44.824803,55 -73.164637,44.82479,54.2 -73.16464999999999,44.82478,53.7 -73.16465700000001,44.824778,53.89999999999999 -73.164658,44.824777,53.6 -73.16466200000001,44.824772,53 -73.164677,44.824757,52.39999999999999"
            )
        )
    )
)

# print(etree.tostring(doc, pretty_print=True))

# output a KML file (named based on the Python script)
outfile = open(__file__.rstrip('.py')+'.kml','w')
outfile.write(str(etree.tostring(doc, pretty_print=True), 'utf-8'))

# assert Schema('kml22gx.xsd').validate(doc)