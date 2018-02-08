#include <Arduino.h>
#include <Wire.h>

//#include <SoftPWMServo.h>
#include <Servo.h>

#define DEBUG_SERIAL 1
#define MAX_CMD_BUF 17 
#define CMD_AUTO 0
#define CMD_STR 1
#define CMD_THR 2
#define CMD_TIME 3

enum errorEnumeration{
	RC_SIGNALS_RECEIVED = 0,
	RC_SIGNAL_WAS_LOST = 1,
	RC_SIGNALED_STOP_AUTONOMOUS = 2,
	STEERING_VALUE_OUT_OF_RANGE = 3,
	THROTTLE_VALUE_OUT_OF_RANGE= 4,
	RUN_AUTONOMOUSLY = 5,
	STOP_AUTONOMOUS = 6,
	STOPPED_AUTO_COMMAND_RECEIVED = 7,
	NO_COMMAND_AVAILABLE = 8,
	GOOD_COMMAND_RECEIVED = 9,
	TOO_MANY_VALUES_IN_COMMAND = 10
};

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

const int PIN_STR = 9;
const int PIN_THR = 7;
const int PIN_IN_STR = 13;
const int PIN_IN_THR = 12;

unsigned long last_serial_time;
unsigned long last_time;
boolean BLINK = true;
boolean gIsInAutonomousMode;

// shoot through delay
int PREV_DIR = LOW;
const int SHOOT_DELAY = 250;

Servo ServoSTR;
Servo ServoTHR;

/*
	Define IMU mpu9250 values
*/
#define		MPU9250_ADDRESS						0x68
#define		MAG_ADDRESS								0x0C

#define		GYRO_FULL_SCALE_250_DPS		0x00	
#define		GYRO_FULL_SCALE_500_DPS		0x08
#define		GYRO_FULL_SCALE_1000_DPS	 0x10
#define		GYRO_FULL_SCALE_2000_DPS	 0x18

#define		ACC_FULL_SCALE_2_G				0x00	
#define		ACC_FULL_SCALE_4_G				0x08
#define		ACC_FULL_SCALE_8_G				0x10
#define		ACC_FULL_SCALE_16_G			 0x18

#define WHO_AM_I_MPU9250 0x75 // Should return 0x71



// This function read Nbytes bytes from I2C device at address Address. 
// Put read bytes starting at register Register in the Data array. 
void I2Cread(uint8_t Address, uint8_t Register, uint8_t Nbytes, uint8_t* Data)
{
	// Set register address
	Wire.beginTransmission(Address);
	Wire.write(Register);
	Wire.endTransmission();
	
	// Read Nbytes
	Wire.requestFrom(Address, Nbytes); 
	uint8_t index=0;
	while (Wire.available())
		Data[index++]=Wire.read();
}



// Write a byte (Data) in device (Address) at register (Register)
void I2CwriteByte(uint8_t Address, uint8_t Register, uint8_t Data)
{
	// Set register address
	Wire.beginTransmission(Address);
	Wire.write(Register);
	Wire.write(Data);
	Wire.endTransmission();
}


int initIMU() {
	 // Set accelerometers low pass filter at 5Hz
	I2CwriteByte(MPU9250_ADDRESS,29,0x06);
	// Set gyroscope low pass filter at 5Hz
	I2CwriteByte(MPU9250_ADDRESS,26,0x06);
 
	
	// Configure gyroscope range
	I2CwriteByte(MPU9250_ADDRESS,27,GYRO_FULL_SCALE_1000_DPS);
	// Configure accelerometers range
	I2CwriteByte(MPU9250_ADDRESS,28,ACC_FULL_SCALE_4_G);
	// Set by pass mode for the magnetometers
	I2CwriteByte(MPU9250_ADDRESS,0x37,0x02);
	// Request continuous magnetometer measurements in 16 bits
	I2CwriteByte(MAG_ADDRESS,0x0A,0x16);

}

void setup() {
	Wire.begin();
	Serial.begin(9600);
	delay(250);

	pinMode(PIN_IN_STR, INPUT);
	pinMode(PIN_IN_THR, INPUT);
	
	ServoSTR.attach(PIN_STR);
	ServoTHR.attach(PIN_THR);

	initIMU();
	gIsInAutonomousMode = false;
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

void sendSerialConstantCommand( int theCommand ){
	commandDataStruct theCommandData;
	const int someNonZeroValue = 55;
	
	theCommandData.command = theCommand;
	theCommandData.ax = someNonZeroValue;
	theCommandData.ay = someNonZeroValue;
	theCommandData.az = someNonZeroValue;
	theCommandData.gx = someNonZeroValue;
	theCommandData.gy = someNonZeroValue;
	theCommandData.gz = someNonZeroValue;
	theCommandData.time = someNonZeroValue;
	theCommandData.str = someNonZeroValue;
	theCommandData.thr = someNonZeroValue;
	sendSerialCommand( &theCommandData );	
}

int getSerialCommandIfAvailable( commandDataStruct *theDataPtr ){
	// http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
	int cmd_cnt = 0;
	
	// the buffer is 1 bigger than the max. size because strtok requires a null byte '0' on the end of the string
	char cmdBuf[MAX_CMD_BUF + 1];

	if (Serial.available() > 0) {		
		byte size = Serial.readBytes(cmdBuf, MAX_CMD_BUF);
	
		// tack on a null byte to the end of the line
		cmdBuf[size] = 0;
	
		// strtok splits a C string into substrings, based on a separator character
		char *command = strtok(cmdBuf, ",");	//  get the first substring

		// loop through the substrings, exiting when the null byte is reached
		//	at the end of each pass strtok gets the next substring
		
		while (command != 0) {		
			switch (cmd_cnt) {
			case CMD_AUTO:
				theDataPtr->command = atoi(command);	
				break;
			case CMD_STR:
				theDataPtr->str = atoi(command);	
				if( theDataPtr->str > 2000 || theDataPtr->str < 1000 ){
					return( STEERING_VALUE_OUT_OF_RANGE );
				}
				break;
				
			case CMD_THR:
				theDataPtr->thr = atoi(command);	
				if( theDataPtr->thr > 2000 || theDataPtr->thr < 1000 ){
					return( THROTTLE_VALUE_OUT_OF_RANGE );
				}
				break;
				
			case CMD_TIME:
				theDataPtr->time = atoi(command);	
				break;
				
			default:
				if (DEBUG_SERIAL) {
					Serial.println("NOOP");
				}
				return( TOO_MANY_VALUES_IN_COMMAND ); 
			}
			
			// Get the next substring from the input string
			// changing the first argument from cmdBuf to 0 is the strtok method for subsequent calls
			command = strtok(0, ",");
			cmd_cnt++;

			if (cmd_cnt == 4) {
				if (DEBUG_SERIAL) {
					Serial.print(theDataPtr->command);
					Serial.print(", ");
					Serial.print(theDataPtr->str);
					Serial.print(", ");
					Serial.print(theDataPtr->thr);
					Serial.print(",");
					Serial.print(theDataPtr->time);
					Serial.println();
				}
				return( GOOD_COMMAND_RECEIVED );
			}
		}
	}
	
	else{
		return( NO_COMMAND_AVAILABLE );
	}
}

int handleRCSignals( int *str_val_ptr, int *thr_val_ptr ) {

	const unsigned long STR_MIN = 1200;
	const unsigned long STR_MAX = 1800;
	const unsigned long THR_MIN = 1250;
	const unsigned long THR_MAX = 1650;
	int result;
	
	unsigned long STR_VAL = pulseIn(PIN_IN_STR, HIGH, 25000); // Read pulse width of
	unsigned long THR_VAL = pulseIn(PIN_IN_THR, HIGH, 25000); // each channel

	if (STR_VAL == 0) {	// no steering RC signal 											// Turn off when not in auto
		if (DEBUG_SERIAL) {
			Serial.println("Out of Range or Powered Off\n");
		}
		result = RC_SIGNAL_WAS_LOST;
	}
		
	else if ( gIsInAutonomousMode ) {
		if( THR_VAL < 1400 ){	// user put it in reverse to turn off autonomous 										// Turn off when not in auto
			if (DEBUG_SERIAL) {
				Serial.println("User wants to halt autonomous\n");
			} 
		result = RC_SIGNALED_STOP_AUTONOMOUS;
		}
	} 
	
	else {	// clip the RC signals to more car appropriate ones
		if( STR_VAL > STR_MAX )
			STR_VAL = STR_MAX;

		else if( STR_VAL < STR_MIN )
			STR_VAL = STR_MIN;

		if( THR_VAL > THR_MAX )
			THR_VAL = THR_MAX;

		else if( THR_VAL < THR_MIN )
			THR_VAL = THR_MIN;
			
		result = RC_SIGNALS_RECEIVED;
	}

	uint8_t Buf[14];
	I2Cread(MPU9250_ADDRESS,0x3B,14,Buf);

	// Create 16 bits values from 8 bits data
	// Accelerometer
	int16_t ax=-(Buf[0]<<8 | Buf[1]);
	int16_t ay=-(Buf[2]<<8 | Buf[3]);
	int16_t az=Buf[4]<<8 | Buf[5];

	// Gyroscope
	int16_t gx=-(Buf[8]<<8 | Buf[9]);
	int16_t gy=-(Buf[10]<<8 | Buf[11]);
	int16_t gz=Buf[12]<<8 | Buf[13];
	
	// _____________________
	// :::	Magnetometer ::: 
	// Read register Status 1 and wait for the DRDY: Data Ready
	// I2Cread(MAG_ADDRESS,0x02,1,&ST1);
	// Read magnetometer data	
	//uint8_t Mag[7];	
	//I2Cread(MAG_ADDRESS,0x03,7,Mag);		
	// Create 16 bits values from 8 bits data 
	// Magnetometer
	//int16_t mx=-(Mag[3]<<8 | Mag[2]);
	//int16_t my=-(Mag[1]<<8 | Mag[0]);
	//int16_t mz=-(Mag[5]<<8 | Mag[4]);	
		
	*thr_val_ptr = (int) THR_VAL;
	*str_val_ptr = (int) STR_VAL;
	
	return( result );
}

void loop() {	
	int result;
	int str_val, thr_val;
	commandDataStruct theCommandData;
	bool autoShouldBeStopped = false;
	
	result = handleRCSignals( &str_val, &thr_val );		// this function will set str_val and thr_val via the pointers
	
	if( result == RC_SIGNALS_RECEIVED ){
		theCommandData.time = millis();
		sendSerialCommand( &theCommandData );
	}
	
	//	The signal for stopping autonomous driving is user putting car in reverse
	//	   this can be a normal operation in manual driving, so a test for auto mode is made

	else if( result == RC_SIGNALED_STOP_AUTONOMOUS ) {
		if( gIsInAutonomousMode )
			autoShouldBeStopped = true;
	}
		
	else if( result == RC_SIGNAL_WAS_LOST ) 
		autoShouldBeStopped = true;
		
	else{
		// future use
	}
	
	if( autoShouldBeStopped ){
		int serialCommandReceived = NO_COMMAND_AVAILABLE;	// setup to get at least one pass thru while loop
	
		while( serialCommandReceived != STOPPED_AUTO_COMMAND_RECEIVED ){	// loop until pi acknowledges STOP auto
			sendSerialConstantCommand( STOP_AUTONOMOUS );
			serialCommandReceived = getSerialCommandIfAvailable( &theCommandData );
		}
		
		str_val = 1500;
		thr_val = 1500;	
		gIsInAutonomousMode = false;
	}
	
	result = getSerialCommandIfAvailable( &theCommandData );
	
	if( result != NO_COMMAND_AVAILABLE ){		// if there is a command, process it
		if ( result != GOOD_COMMAND_RECEIVED ){
			// ignore bad command
		}

		else{	// some sort of good command received
			if( theCommandData.command == RUN_AUTONOMOUSLY ){
				str_val = theCommandData.str;
				thr_val = theCommandData.thr;
				gIsInAutonomousMode = true;
			}
			
			else if( theCommandData.command == STOP_AUTONOMOUS ){
				sendSerialConstantCommand( STOPPED_AUTO_COMMAND_RECEIVED );
				str_val = 1500;
				thr_val = 1500;
				gIsInAutonomousMode = false;
			}			
			
			else{
				// for new commands
			}
		}
	}

	//	write either RC or autonomous str_val and thr_val ( whichever ones were set last )
	ServoSTR.writeMicroseconds( str_val );
	ServoTHR.writeMicroseconds( thr_val );

	//  delay ???
}
