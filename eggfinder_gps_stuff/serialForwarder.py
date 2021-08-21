"""
A simple test server that returns a random number when sent the text "temp" via Bluetooth serial.
"""

import os
import glob
import time
import random

from bluetooth import *

import serial
import serial.tools.list_ports


ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    print('Find port '+ port.device)
ser = serial.Serial(port.device)
if ser.isOpen():
    ser.close()

ser = serial.Serial(port.device, 9600, timeout=1)
ser.flushInput()
ser.flushOutput()
print('Connect ' + ser.name)

import datetime
d = datetime.datetime.fromtimestamp(time.time()).strftime("%b_%d_%y_%H_%M_%S")
f = open(f"out_{d}.txt", "a")

server_sock = BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "TestServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

print("Waiting for connection on RFCOMM channel %d" % port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

from pynmeagps import NMEAReader
import pynmea2
from datetime import datetime

while True:          

    try:
        data = ser.readline().decode('ascii', errors='replace')
        f.write(data.strip())

        try:
            parsed = pynmea2.parse(str(data))
            rxtime = parsed.timestamp.strftime("%H:%M:%S")

            print(f"{parsed.latitude} {parsed.lat_dir},\t{parsed.longitude} {parsed.lon_dir},\t{parsed.altitude} {parsed.altitude_units} at {rxtime} - {parsed.num_sats} sats, quality = {parsed.gps_qual}")
        except Exception as e:
            pass

        f.flush()
        client_sock.send(data)

    except IOError:
        pass

    except KeyboardInterrupt:

        print("disconnected")

        client_sock.close()
        server_sock.close()
        print("all done")

        break
    except Exception:
        pass