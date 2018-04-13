#include <Arduino.h>

struct commandDataStruct {
  int command;
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

commandDataStruct theData;

void setup() {
  Serial.begin(9600);      // open the serial port at 9600 bps:    
  theData.command = 0;
  theData.ax = 0;
  theData.ay = 0;
  theData.az = 0;
  theData.gx = 0;
  theData.gy = 0;
  theData.gz = 0;
  theData.time = 0;
  theData.str = 0;
  theData.thr = 0;
}

void modStruct( commandDataStruct *theDataPtr ){

  theDataPtr->ay = theDataPtr->ay - 1;
}

void sendSerialCommand( commandDataStruct *theDataPtr ){
  Serial.flush();
  Serial.print(theDataPtr->command);
  Serial.print(",");
  Serial.print(theDataPtr->ax);
  Serial.print(",");
  Serial.print(theDataPtr->ay);
  Serial.print(",");
  Serial.print(theDataPtr->az);
  Serial.print(",");
  Serial.print(theDataPtr->gx);
  Serial.print(",");
  Serial.print(theDataPtr->gy);
  Serial.print(",");
  Serial.print(theDataPtr->gz);
  Serial.print(",");
  Serial.print(theDataPtr->time);
  Serial.print(",");
  Serial.print(theDataPtr->str);
  Serial.print(",");
  Serial.print(theDataPtr->thr);
  Serial.println();
}

void loop() {
    
  theData.ax = theData.ax + 1;
  sendSerialCommand( &theData );
  modStruct( &theData );
  sendSerialCommand( &theData );
  delay(500);
}
