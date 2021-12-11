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
import datetime
import pynmea2
from datetime import datetime
import threading

d = datetime.fromtimestamp(time.time()).strftime("%b_%d_%y_%H_%M_%S")
csvOutputFile = open(f"out_{d}.txt", "a")
print(csvOutputFile)

ser = None
client_sock_list = []
server_sock = None


def advertise_bluetooth():
    print("Starting Bluetooth")
    global server_sock
    server_sock = BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "TestServer",
                    service_id = uuid,
                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ], 
                        )
    while True:
        print("Waiting for connection on RFCOMM channel %d" % port)
        # client_sock, client_info = server_sock.accept()
        cs, ci = server_sock.accept()
        global client_sock_list
        client_sock_list.append(cs)
        client_info = ci
        print("Accepted connection from ", client_info)

def find_serial_port():
    ports = serial.tools.list_ports.comports(include_links=False)
    for port in ports :
        print('Found device at port '+ port.device)
    if ports == [] or port is None:
        raise ConnectionError("No devices found!")
    global ser
    ser = serial.Serial(port.device)
    if ser.isOpen():
        ser.close()

    ser = serial.Serial(port.device, 9600, timeout=1)
    ser.flushInput()
    ser.flushOutput()
    print('Connected to ' + ser.name)

def send_bluetooth(dataString, parsed, time):
        for cs in client_sock_list:
            try:
                cs.send(dataString)
            except Exception as e:
                print(f"Lost BT from {cs.getpeername()}")
                cs.close()
                client_sock_list.remove(cs)

def print_stuff(dataString, parsed, rxtime):
    try:
        if hasattr(parsed, "latitude"):
            print(f"{parsed.latitude},\t{parsed.longitude},\t{parsed.altitude}{parsed.altitude_units} at {rxtime} - {parsed.num_sats} sats, quality = {parsed.gps_qual} - " +\
                f"https://www.google.com/maps/place/{parsed.latitude}+{parsed.longitude}")
        if hasattr(parsed, 'mode_fix_type'):
            print(f"Fix Type: {['None','2D','3D'][int(parsed.mode_fix_type) - 1]}")
    except Exception as e:
        print(e)

def write_string(dataString, parsed, time):
    try:
        csvOutputFile.write(dataString.strip())
        csvOutputFile.write('\n')
        csvOutputFile.flush()
    except Exception as e:
        print(e)

def serial_loop():
    while True: 
        try:
            data = ser.readline().decode('ascii', errors='replace')
            #time.sleep(1)

            try:
                parsed = pynmea2.parse(str(data))
                if not parsed.is_valid:
                    print("Invalid packet!")
                    continue
                rxtime = parsed.timestamp.strftime("%H:%M:%S")

                write_string(data, parsed, rxtime)
                print_stuff(data, parsed, rxtime)
                send_bluetooth(data, parsed, rxtime)
            except Exception as e:
                pass

        except IOError as e:
            print(e)
        except KeyboardInterrupt:

            print("disconnected")

            if client_sock_list != []:
                for c in client_sock_list:
                    c.close()
            if server_sock is not None:
                server_sock.close()
            print("all done")

            break
        except Exception:
            pass

find_serial_port()
threading.Thread(target=advertise_bluetooth).start()
# advertise_bluetooth()
serial_loop()

# data = "$GPGGA,215338.000,4449.6176,N,07310.3220,W,1,04,4.9,46.5,M,-32.1,M,,0000*5E"
# parsed = pynmea2.parse(str(data))
# rxtime = parsed.timestamp.strftime("%H:%M:%S")
# print_stuff(data, parsed, rxtime)
# send_bluetooth(data, parsed, rxtime)