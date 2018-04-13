#include <Arduino.h>
#include <Servo.h>

// pi need not be on
// ESC switch must be on 

const int PIN_STR = 9;
const int PIN_THR = 7;
const int PIN_IN_STR = 13;
const int PIN_IN_THR = 12;


Servo ServoSTR;
Servo ServoTHR;

struct commandDataStruct {
int command;
int16_t ax;		// acceleration
int16_t ay;
int16_t az;
int16_t gx;		// yaw
int16_t gy;		// pitch
int16_t gz;		// roll
unsigned long time;	// millis
int str;		// steering 1000-2000
int thr;		// throttle 1000-2000
// int checksum;	someday???
};

void handleRCSignals( commandDataStruct *theDataPtr ) {

	const unsigned long STR_MIN = 1200;
	const unsigned long STR_MAX = 1800;
	const unsigned long THR_MIN = 1250;
	const unsigned long THR_MAX = 1650;
	
	while( 1 ){
		unsigned long STR_VAL = pulseIn(PIN_IN_STR, HIGH, 25000); // Read pulse width of
		unsigned long THR_VAL = pulseIn(PIN_IN_THR, HIGH, 25000); // each channel

		Serial.print("  PINS: ");
		Serial.print(PIN_IN_STR);
		Serial.print(",");
		Serial.print(PIN_IN_THR);
		Serial.println();
		
		Serial.print(STR_VAL);
		Serial.print(",");
		Serial.print(THR_VAL);
		Serial.println();
	}
	
}

	
	
void setup()
{
	Serial.begin(9600);
	pinMode(PIN_IN_STR, INPUT);
	pinMode(PIN_IN_THR, INPUT);

	ServoSTR.attach(PIN_STR);
	ServoTHR.attach(PIN_THR);
	
}

void loop()
{
	commandDataStruct theCommandData;
	bool autoShouldBeStopped = false;
	
	handleRCSignals( &theCommandData );
}


#if 0
void loop()
{
	unsigned long STR_VAL = pulseIn(PIN_IN_STR, HIGH, 25000); // Read the pulse width of
	unsigned long THR_VAL = pulseIn(PIN_IN_THR, HIGH, 25000); // each channel
	Serial.print(STR_VAL);
	Serial.print(",");
	Serial.print(THR_VAL);
	Serial.println();
	Serial.println();
	delay( 500 );
}
#endif