#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <Wire.h>

#define OLED_RESET 4
// Adafruit_SSD1306 display1(OLED_RESET);
// Adafruit_SSD1306 display2(OLED_RESET);


#define READ_PIN      A2
#define PWM_PIN       11
#define ADJ_PIN       A1
 
int Buzzpin=12;
long i=1023; 
float voltage;

byte data[128];
int x;
int y1,y2;
double y, pwmVolts;
unsigned long Time, Timenow, Interval=0;


char* myStrings[]={"Voltage","Current","Resistance","Continuity Test","Oscilloscope","Miscellaneous"};         // options to show in the menu


//mapping potentiometer int
int potMap=0;
int boxes;
int width;
char options;
int R1=4800;  
int R2=5200;   
int R4=4630;
int R3=5250;
float Supplyvoltage;
void setup()   {                
  Serial.begin(9600);
  // init done
  pinMode(Buzzpin, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  
  pinMode(READ_PIN, INPUT);
  pinMode(ADJ_PIN, INPUT);
  pinMode(PWM_PIN, OUTPUT);
 
  Supplyvoltage= readVcc();
  Serial.print(Supplyvoltage);
  // display1.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  // display1.clearDisplay();
  // display1.display();

  // display2.begin(SSD1306_SWITCHCAPVCC, 0x3D);
  // display2.clearDisplay();
  // display2.display();

}

long readVcc() {
  // Read 1.1V reference against AVcc
  // set the reference to Vcc and the measurement to the internal 1.1V reference
  #if defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
    ADMUX = _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  #elif defined (__AVR_ATtiny24__) || defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny84__)
    ADMUX = _BV(MUX5) | _BV(MUX0);
  #elif defined (__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
    ADMUX = _BV(MUX3) | _BV(MUX2);
  #else
    ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  #endif  

  delay(2); // Wait for Vref to settle
  ADCSRA |= _BV(ADSC); // Start conversion
  while (bit_is_set(ADCSRA,ADSC)); // measuring

  uint8_t low  = ADCL; // must read ADCL first - it then locks ADCH  
  uint8_t high = ADCH; // unlocks both

  long result = (high<<8) | low;

  result = 1125300L / result; // Calculate Vcc (in mV); 1125300 = 1.1*1023*1000
  result= result;
  return result; // Vcc in millivolts
}



void ReadVoltage(){
 
  int sensorValueVolt = analogRead(A0);
  voltage = (((R1+R2)/R1) * (((readVcc()) *sensorValueVolt*.001)/ 1023));  //3.1k ohms 21.8 k ohms
  // display2.drawRect(1, 20, display1.width()-10, display1.height()-20, WHITE);
  // display2.setTextSize(1);
  // display2.setTextColor(WHITE);
  // display2.setCursor(10,25);
  // display2.print("Voltage: ");
  // display2.println(voltage);
  // display2.display();
  Serial.println(sensorValueVolt);
  Serial.println(readVcc(),DEC);
  Serial.println(voltage);
  delay(100);
  

}

void ContinuityTester(){


  // display2.drawRect(1, 20, display2.width()-10, display2.height()-20, WHITE);  
  int sensorValueCon = analogRead(A0);
  if(sensorValueCon>10){
    int resistance = ((i*R1)/(sensorValueCon))-(R1+R2);
    // display2.setTextSize(1);
    // display2.setTextColor(WHITE);
    // display2.setCursor(10,25);
    // display2.print("Continuity: ");
    // display2.display();
    if(resistance<80){
      tone(Buzzpin,500,50);
      Serial.println("Continuity!");
      // display2.setCursor(80,25);
      // display2.println("Yes");
      // display2.display();
      delay(50);
    } else {
      noTone(Buzzpin);
      Serial.println("NO Continuity");
      // display2.setCursor(80,25);
      // display2.println("NO");
      // display2.display();
    }
  }
  else{
    // display2.setCursor(10,25);  
    // display2.print("Connect Object");  
    digitalWrite(Buzzpin,LOW);
    // display2.display();
    Serial.println("Connect Object");
  }
    // display2.display();
}


void ResistanceMeter(){
  
  // display2.clearDisplay();
  // display2.drawRect(1, 20, display2.width()-10, display2.height()-20, WHITE);  
  int sensorValueResistance = analogRead(A0);
  if(sensorValueResistance>15){
  int resistance = ((i*R1)/(sensorValueResistance))-(R1+R2);  // Resistance= (R3*Vb)/(Vr3) - (R2+R3)
  // display2.setTextSize(1);
  // display2.setTextColor(WHITE);
  // display2.setCursor(10,25);
  // display2.print("Resistance: ");
  // display2.println(resistance);
  Serial.println("Resistance: ");
  Serial.println(resistance);

  }
  else{
  // display2.setCursor(10,25);  
  // display2.print("Connect Resistor");  
  Serial.println("Please connect a resistor first");
  }
  // display2.display();
  
}

void Miscellaneous(){
  // display2.clearDisplay();
  // display2.drawRect(1, 20, display2.width()-10, display2.height()-20, WHITE);  
  // display2.setTextSize(1);
  // display2.setTextColor(WHITE);
  // display2.setCursor(10,25);
  // display2.print("WIP");
  // display2.display();
  
}


void Oscilloscope(){
  
//   pwmVolts = analogRead(ADJ_PIN) / 4 ;
//   analogWrite(PWM_PIN, pwmVolts);
//   // draw the axis, lables and tick marks
//   for (int y = 0; y < 6; y++) {
//     display2.drawFastHLine(7, y * (48) / 5 + 16, 3, WHITE);
//   }
//   // don't forget to set the back color arguement otherwise numbers may draw on the previous number
//   display2.setTextColor(WHITE, BLACK);
//   display2.setTextSize(1);
//   display2.setCursor(0, 57);
//   display2.println("0");
//   display2.setCursor(0, 16);
//   display2.println("5");

//   display2.fillRect(0, 0,  127 , 14, WHITE);
//   display2.setTextColor(BLACK, WHITE);
//   display2.drawFastHLine(10, 63,  128 - 10, WHITE);
//   display2.drawFastVLine(10, 16,  63, WHITE);
//   display2.setTextSize(1);
//   display2.setCursor(2, 3);
//   display2.print("Scope");
//   display2.print(Interval);
//   display2.print("    ");
//   display2.print(readVcc(),DEC);
//   int TimetoStop=15000;      // set timetostop to whatever you want the interval to be
//   int TimeInt=(TimetoStop-13500)/126;
//       if(TimeInt<0){
//         TimeInt=0;
//       }

    
//    //  while(analogRead(READ_PIN)<20){      
//    //   delayMicroseconds(1);
//  //   } 
//     Time=micros();
//    for (x = 10; x <= 127; x++) {
//     data[x] = (analogRead(READ_PIN));  
//    delayMicroseconds(TimeInt);  
//    /* while((Timenow-Time)< (TimeInt)){
//        Timenow=micros();
//        Serial.println("Waiting");
//    }
//    */
//     }
//     Timenow=micros();
//     Interval=Timenow-Time;
//  Serial.println(Interval);
     
//    for (x = 10; x <= 127; x++){
//     y1= 4 * (((data[x-1 ])*readVcc()) / ((21.7659)*5*1000));           // ********** remove the 4* factor if your data doesn't fit in the screen. I simply couldn't solve an error, so I kept it.  
//     y2= 4 * (((data[x ])*readVcc()) / ((21.7659)*5*1000));             // ********** remove the 4* factor if your data doesn't fit in the screen. I simply couldn't solve an error, so I kept it.  
//   display2.drawLine(x , 63- y1, x , 63- y2 , WHITE);
//    }   
 
// display2.display();
  
}



void mapPot(){
  int sensorValuePot = analogRead(A1);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
 float pot = sensorValuePot* (10000/5115);
  // print out the value you read:
  pot= map (pot, 0, 1010,0,boxes-1);
  potMap=pot;
  width= 128/boxes;
  Serial.print(pot);
}

void mainMenu(){
 boxes=6;
  mapPot();
  // display1.drawRect(0, 18, 128, 18, WHITE);
  // display1.setTextSize(1);
  // display1.setTextColor(WHITE);
  // display1.setCursor(5,24);
  // display1.print(myStrings[potMap]);
  // display1.setCursor(5,24+16);
  // display1.print(myStrings[potMap+1]);
  // display1.setCursor(5,24+32);
  // display1.print(myStrings[potMap+2]);
  // display1.setCursor(5,24+48);
  // display1.print(myStrings[potMap+3]);
  
  // BatteryStatus();
  
  // display1.display();
  // display1.drawRect(potMap*width, 0, width, 16, WHITE); 
  // delay(5);
  // display1.clearDisplay();

  Serial.println("Where would you like to go?");
  Serial.println("(1) Read Voltage");
  Serial.println("(2) Read Resistance");
  Serial.println("(3) Test Continuity");
  Serial.println("(4) Osmelloscope (BROKEN)");
   
}


void readpushButton(){
   if(digitalRead(2)==0){
    while(digitalRead(2)==0){
          delay(5);
        }
   
    switch (potMap) {
    case 0:
      while(1==1){
      // display1.clearDisplay();
      ReadVoltage();
      delay(100);
      if(digitalRead(3)==0){
        while(digitalRead(3)==0){
          delay(5);
        }
        delay(100);
        // display2.clearDisplay();
        // display2.display();
        break;
      }
      
     }
     break;
    
    case 2: 

    while(1==1){
      // display2.clearDisplay();
     ResistanceMeter();
      delay(100);
      if(digitalRead(3)==0){
        while(digitalRead(3)==0){
          delay(5);
        }
        delay(100);
        // display2.clearDisplay();
        // display2.display();
        break;
      }
     }
      break; 

    case 3: 
      while(1==1){
      // display2.clearDisplay();
      ContinuityTester();
      delay(100);
      if(digitalRead(3)==0){
        while(digitalRead(3)==0){
          delay(5);
        }
        delay(100);
        // display2.clearDisplay();
        // display2.display();
        break;
      }
     }
      break;

     case 4: 
      while(1==1){
      // display2.clearDisplay();
      Oscilloscope();
      if(digitalRead(3)==0){
        while(digitalRead(3)==0){
          delay(5);
        }
        // display2.clearDisplay();
        // display2.display();
        delay(100);
        break;
      }
     }
      break;

 
    case 5: 
      while(1==1){
      // display2.clearDisplay();
      Miscellaneous();
      delay(100);
      if(digitalRead(3)==0){
        while(digitalRead(3)==0){
          delay(5);
        }
        delay(100);
        // display2.clearDisplay();
        // display2.display();
        break;
      }
     }
      break;
      
    default:
      break;
    }
   }
 
}



void loop() {
   mainMenu();
   readpushButton();
}
