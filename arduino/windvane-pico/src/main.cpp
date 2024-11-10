#include <Arduino.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define POT_PIN PIN_A1
#define BUS_PIN PIN_A0

#define ANALOG_MAX (1 << 10)

template <typename T>
inline T map_t(T x, T in_min, T in_max, T out_min, T out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
  // default to 10 bits of precision
  pinMode(POT_PIN, INPUT);
  pinMode(BUS_PIN, INPUT);

  // USB bus
  Serial.begin(115200);
  // Serial1 tx on pin 1, rx on pin 2
  Serial1.begin(115200);
}

void loop() {
    // Read in angle and remap. Might need to invert the polarity/apply calibration later
    int busPinRaw = analogRead(BUS_PIN);
    float busVoltage = map_t<float>(busPinRaw, 0, ANALOG_MAX, 0.0, 3.3) * 2.0;
    float scaleFactor = busVoltage / 5.0;

    // TODO calibrate the voltage divider
    int windvnPinRaw = analogRead(POT_PIN);
    float windvnVoltage = map_t<float>(windvnPinRaw, 0, ANALOG_MAX, 0, 3.3) * 2.0;
    // 6127V1A360L.5FS - 0.2 V to 4.8 V output
    int dir = roundf(map_t<float>(windvnVoltage, 0.2 * scaleFactor, 4.8 * scaleFactor, 0, 360));

    Serial.print("Bus voltage: ");
    Serial.print(static_cast<double>(busVoltage));
    Serial.print(" Windvn voltage: ");
    Serial.print(static_cast<double>(windvnVoltage));
    Serial.print(" dir: ");
    Serial.println(dir);

    // Create message, up until checksum
    char str[100];
    int len = snprintf(str, sizeof(str), 
        "$WIMWV,%i,R,,,A", dir);

    // calculate checksum
    uint8_t checksum = 0;
    for (int i = 1; i < len; i++) {
        checksum ^= str[i];
    }

    // append checksum+newlines to message
    snprintf(str+len, sizeof(str)-len+4, "*%X%X\r\n", (checksum >> 4) & 0x0f, checksum & 0x0f);

    Serial.print(str);
    Serial1.print(str);

    // And rate limit to say 10hz lol
    delay(100);
}
