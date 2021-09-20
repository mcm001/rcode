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

# ports = serial.tools.list_ports.comports(include_links=False)
# for port in ports :
#     print('Found device at port '+ port.device)
# if ports == [] or port is None:
#     raise ConnectionError("No devices found!")
# ser = serial.Serial(port.device)
# if ser.isOpen():
#     ser.close()

# ser = serial.Serial(port.device, 9600, timeout=1)
# ser.flushInput()
# ser.flushOutput()
# print('Connected to ' + ser.name)

import datetime
d = datetime.datetime.fromtimestamp(time.time()).strftime("%b_%d_%y_%H_%M_%S")
f = open(f"out_{d}.txt", "a")

server_sock = BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# advertise_service( server_sock, "TestServer",
#                    service_id = uuid,
#                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
#                    profiles = [ SERIAL_PORT_PROFILE ], 
# #                   protocols = [ OBEX_UUID ] 
#                     )
# print("Waiting for connection on RFCOMM channel %d" % port)
# client_sock, client_info = server_sock.accept()
# print("Accepted connection from ", client_info)

import pynmea2
from datetime import datetime
import threading

def send_bluetooth(dataString, parsed, time):
    try:
        client_sock.send(dataString)
    except Exception as e:
        print(e)

def print_stuff(dataString, parsed, time):
    try:
        if hasattr(parsed, "latitude"):
            print(f"{parsed.latitude},\t{parsed.longitude},\t{parsed.altitude}{parsed.altitude_units} at {rxtime} - {parsed.num_sats} sats, quality = {parsed.gps_qual}")
            print(f"https://www.google.com/maps/place/{parsed.latitude}+{parsed.longitude}")
        if hasattr(parsed, 'mode_fix_type'):
            print(f"Fix Type: {['None','2D','3D'][int(parsed.mode_fix_type) - 1]}")
    except Exception as e:
        print(e)

def write_string(dataString, parsed, time):
    try:
        f.write(dataString.strip())
        f.flush()
    except Exception as e:
        print(e)

def serial_task():
    while True: 
        try:
            data = ser.readline().decode('ascii', errors='replace')

            try:
                parsed = pynmea2.parse(str(data))
                rxtime = parsed.timestamp.strftime("%H:%M:%S")

                write_string(data, parsed, rxtime)
                print_stuff(data, parsed, rxtime)
                send_bluetooth(data, parsed, rxtime)
            except Exception as e:
                pass

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

# serial_task()
data = "$GPGGA,215338.000,4449.6176,N,07310.3220,W,1,04,4.9,46.5,M,-32.1,M,,0000*5E"
parsed = pynmea2.parse(str(data))
rxtime = parsed.timestamp.strftime("%H:%M:%S")
print_stuff(data, parsed, rxtime)