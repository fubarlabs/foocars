#include <Arduino.h>

struct carDataStruct {
  float ax;		// acceleration
  float ay;
  float az;
  float gx;		// yaw
  float gy;		// pitch
  float gz;		// roll
  unsigned long time;	// millis
  int str;		// steering 1000-2000
  int thr;		// throttle 1000-2000
  // int checksum;	someday???
};


void setup() {
  Serial.begin(9600);      // open the serial port at 9600 bps:    
}

void modStruct( carDataStruct *theDataPtr ){

  theDataPtr->ax = 20.0;
}

void loop() {
    
  carDataStruct theData;
  theData.ax = 10.0;
  Serial.println( theData.ax );
  modStruct( &theData );
  Serial.println ( theData.ax );
  Serial.println ( "" );
  delay(500);
}
