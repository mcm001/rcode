import struct
import time

import serial
from serial.tools.list_ports import comports
import pandas as pd

SERIAL_READ_SIZE = 2048
# OUTPUT_POST_CSV_NAME = "D:\\Downloads\\superguppy-fcb.csv"
OUTPUT_POST_CSV_NAME = ("D:\\Downloads\\fcbv0-11-20-2021-carby.csv")
# OUTPUT_POST_CSV_NAME = ("D:\\Documents\\GitHub\\fcb-offloader-standalone\\output_data\\output-post.csv")
MAX_CODE_LOOP_PERIOD_S = 0.02  # Slower than actual to prevent buffer overrun in FCB

ACK = "\r\nOK\r\n"
COMPLETE = "\r\nDONE\r\n\r\n"

struct_pack_str = "<"  # little endian
struct_pack_str += "L"  # uint32_t timestamp_s
struct_pack_str += "L"  # uint32_t timestamp_us
struct_pack_str += "h"  # int16_t imu1_accel_x_raw
struct_pack_str += "h"  # int16_t imu1_accel_y_raw
struct_pack_str += "h"  # int16_t imu1_accel_z_raw
struct_pack_str += "d"  # double imu1_accel_x
struct_pack_str += "d"  # double imu1_accel_y
struct_pack_str += "d"  # double imu1_accel_z
struct_pack_str += "h"  # int16_t imu1_gyro_x_raw
struct_pack_str += "h"  # int16_t imu1_gyro_y_raw
struct_pack_str += "h"  # int16_t imu1_gyro_z_raw
struct_pack_str += "d"  # double imu1_gyro_x
struct_pack_str += "d"  # double imu1_gyro_y
struct_pack_str += "d"  # double imu1_gyro_z
struct_pack_str += "h"  # int16_t imu1_mag_x_raw
struct_pack_str += "h"  # int16_t imu1_mag_y_raw
struct_pack_str += "h"  # int16_t imu1_mag_z_raw
struct_pack_str += "d"  # double imu1_mag_x
struct_pack_str += "d"  # double imu1_mag_y
struct_pack_str += "d"  # double imu1_mag_z
struct_pack_str += "h"  # int16_t imu2_accel_x_raw
struct_pack_str += "h"  # int16_t imu2_accel_y_raw
struct_pack_str += "h"  # int16_t imu2_accel_z_raw
struct_pack_str += "d"  # double imu2_accel_x
struct_pack_str += "d"  # double imu2_accel_y
struct_pack_str += "d"  # double imu2_accel_z
struct_pack_str += "h"  # int16_t imu2_gyro_x_raw
struct_pack_str += "h"  # int16_t imu2_gyro_y_raw
struct_pack_str += "h"  # int16_t imu2_gyro_z_raw
struct_pack_str += "d"  # double imu2_gyro_x
struct_pack_str += "d"  # double imu2_gyro_y
struct_pack_str += "d"  # double imu2_gyro_z
struct_pack_str += "h"  # int16_t imu2_mag_x_raw
struct_pack_str += "h"  # int16_t imu2_mag_y_raw
struct_pack_str += "h"  # int16_t imu2_mag_z_raw
struct_pack_str += "d"  # double imu2_mag_x
struct_pack_str += "d"  # double imu2_mag_y
struct_pack_str += "d"  # double imu2_mag_z
struct_pack_str += "h"  # int16_t high_g_accel_x_raw
struct_pack_str += "h"  # int16_t high_g_accel_y_raw
struct_pack_str += "h"  # int16_t high_g_accel_z_raw
struct_pack_str += "d"  # double high_g_accel_x
struct_pack_str += "d"  # double high_g_accel_y
struct_pack_str += "d"  # double high_g_accel_z
struct_pack_str += "d"  # double baro1_pres
struct_pack_str += "d"  # double baro1_temp
struct_pack_str += "d"  # double baro2_pres
struct_pack_str += "d"  # double baro2_temp
struct_pack_str += "f"  # float gps_lat
struct_pack_str += "f"  # float gps_long
struct_pack_str += "f"  # float gps_alt
struct_pack_str += "f"  # float gps_speed
struct_pack_str += "f"  # float gps_course
struct_pack_str += "f"  # float gps_latitude_deviation
struct_pack_str += "f"  # float gps_longitude_deviation
struct_pack_str += "f"  # float gps_altitude_deviation
struct_pack_str += "f"  # float gps_speed_kph
struct_pack_str += "f"  # float gps_speed_knots
struct_pack_str += "i"  # int gps_seconds
struct_pack_str += "i"  # int gps_minutes
struct_pack_str += "i"  # int gps_hours
struct_pack_str += "i"  # int gps_day
struct_pack_str += "i"  # int gps_month
struct_pack_str += "i"  # int gps_year
struct_pack_str += "i"  # int gps_num_sats
struct_pack_str += "c"  # char gps_status
struct_pack_str += "d"  # double battery_voltage
struct_pack_str += "??????"  # bool pyro_continuity[6]

SENSOR_STRUCT_PACK_STR = (
    "<LLhhhdddhhhdddhhhdddhhhdddhhhdddhhhdddhhhdddddddffffffffffQiiiiiiicd??????"
)

print("Available ports listed below")
port_list = list(comports())
ports = [port.device for port in port_list]
for port in ports:
    print(port)

while True:
    if(len(ports) != 1):
        port_dev = input("Enter port name to communicate with: ")
    else:
        port_dev = str(ports[0])
    if port_dev not in ports:
        print("Invalid entered port")
        continue
    break

# Try opening serial port
ser = serial.Serial(port=port_dev, baudrate=9600, timeout=5)

# Ask to start new flight
ser.write("--createFlight\n".encode('utf-8'))
response = ser.read(size=len(ACK)).decode("utf-8")
print(response)
if response != ACK:
    print("Error: new flight not entered")
    exit(-1)

# Tell board to sim
ser.write("--sim\n".encode("utf-8"))
response = ser.read(size=len(ACK)).decode("utf-8")
if response != ACK:
    print("Error: sim not acknowledged")
    exit(-1)
print("Sim command acknowledged - simming now")

# Read output-post.csv
df = pd.read_csv(OUTPUT_POST_CSV_NAME, index_col=0)
df["time_diff"] = df["timestamp_s"].diff().fillna(0)
start_time = time.time()
for row in df.itertuples():
    # Wait for next transmit time
    time_to_wait = max(MAX_CODE_LOOP_PERIOD_S, row.time_diff / 1000.0)
    while time.time() - start_time < time_to_wait:
        continue
    start_time = time.time()
    # Group line into data


    # print(f"{row.gps_lat},{row.gps_long}")

    data = struct.pack(
                SENSOR_STRUCT_PACK_STR,
                row.timestamp_s,
                row.timestamp_ms,
                row.imu1_accel_x,
                row.imu1_accel_y,
                row.imu1_accel_z,
                row.imu1_accel_x_real,
                row.imu1_accel_y_real,
                row.imu1_accel_z_real,
                row.imu1_gyro_x,
                row.imu1_gyro_y,
                row.imu1_gyro_z,
                row.imu1_gyro_x_real,
                row.imu1_gyro_y_real,
                row.imu1_gyro_z_real,
                row.imu1_mag_x,
                row.imu1_mag_y,
                row.imu1_mag_z,
                row.imu1_mag_x_real,
                row.imu1_mag_y_real,
                row.imu1_mag_z_real,
                row.imu2_accel_x,
                row.imu2_accel_y,
                row.imu2_accel_z,
                row.imu2_accel_x_real,
                row.imu2_accel_y_real,
                row.imu2_accel_z_real,
                row.imu2_gyro_x,
                row.imu2_gyro_y,
                row.imu2_gyro_z,
                row.imu2_gyro_x_real,
                row.imu2_gyro_y_real,
                row.imu2_gyro_z_real,
                row.imu2_mag_x,
                row.imu2_mag_y,
                row.imu2_mag_z,
                row.imu2_mag_x_real,
                row.imu2_mag_y_real,
                row.imu2_mag_z_real,
                row.high_g_accel_x,
                row.high_g_accel_y,
                row.high_g_accel_z,
                row.high_g_accel_x_real,
                row.high_g_accel_y_real,
                row.high_g_accel_z_real,
                row.baro1_pres,
                row.baro1_temp,
                row.baro2_pres,
                row.baro2_temp,
                row.gps_lat,
                row.gps_long,
                row.gps_alt,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                "a".encode("utf-8"),
                row.battery_voltage,
                row.pyro_cont,
                row.pyro_cont >> 1,
                row.pyro_cont >> 2,
                row.pyro_cont >> 3,
                row.pyro_cont >> 4,
                row.pyro_cont >> 5,
    )

    # Send data over serial
    ser.write(data)

response = ser.read(size=len(COMPLETE)).decode("utf-8")
if response != COMPLETE:
    print("Error: sim not complete")
    exit(-1)

print("Sim success!")
