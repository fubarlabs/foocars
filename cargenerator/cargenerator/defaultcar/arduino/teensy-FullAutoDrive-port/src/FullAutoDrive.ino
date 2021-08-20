#include <Arduino.h>
#include <Servo.h>

#define DEBUG_SERIAL 1

#define MAX_CMD_BUF 17 
#define CMD_AUTO 0
#define CMD_STR 1
#define CMD_THR 2
#define CMD_TIME 3

// Pin Defines

const int PIN_STR = 21;
const int PIN_THR = 20;
//These lines are for the input capture for pwm read off RC
#define RC_INPUT_STR 3
#define RC_INPUT_THR 4

int chan_a_start, chan_a; 	//Used to keep track of the timing of the edges of Channel A and B.
int chan_b_start, chan_b;
int lastUpdated_a; //This is used to keep track of the last time the
int lastUpdated_b; //signal was sent.  If nothing is sent for 1s, we disable that output by just setting it hard to 1500ms.
IntervalTimer watchdog;

//this lists the states the fubarino side of the car can be in 
enum carStateEnumeration{
    STATE_MANUAL=0,
    STATE_AUTONOMOUS=1,
    STATE_TERM_AUTO=2
};

enum commandEnumeration{
    NOT_ACTUAL_COMMAND = 0,
    RC_SIGNAL_WAS_LOST = 1,
    RC_SIGNALED_STOP_AUTONOMOUS = 2,
    STEERING_VALUE_OUT_OF_RANGE = 3,
    THROTTLE_VALUE_OUT_OF_RANGE= 4,
    RUN_AUTONOMOUSLY = 5,
    STOP_AUTONOMOUS = 6,
    STOPPED_AUTO_COMMAND_RECEIVED = 7,
    NO_COMMAND_AVAILABLE = 8,
    GOOD_PI_COMMAND_RECEIVED = 9,
    TOO_MANY_VALUES_IN_COMMAND = 10,
    GOOD_RC_SIGNALS_RECEIVED = 11
};

struct commandDataStruct {
int command;
int16_t ax;        // acceleration
int16_t ay;
int16_t az;
int16_t gx;        // yaw
int16_t gy;        // pitch
int16_t gz;        // roll
unsigned long time;    // millis
int str;        // steering 1000-2000
int thr;        // throttle 1000-2000
// int checksum;    someday???
};

int gTotalNumberOfPassesForCommandDisplay = 10000;
int gCountOfPassesForCommandDisplay = gTotalNumberOfPassesForCommandDisplay;

unsigned long gCenteredSteeringValue = 1500;
unsigned long gCenteredThrottleValue = 1500;

int gcarState;
int gTheOldRCcommand;
int gTheOldPiCommand;

//these values will be car specific
const unsigned long minimumSteeringValue = 1000;
const unsigned long maximumSteeringValue = 2000;
const unsigned long minimumThrottleValue = 1000;
const unsigned long maximumThrottleValue = 2000;
const unsigned long throttleThresholdToShutdownAuto = 1600;

Servo ServoSTR;
Servo ServoTHR;

void setup() {
    
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    Serial.println( "Starting up..." );
    
    pinMode(RC_INPUT_STR, INPUT);
    pinMode(RC_INPUT_THR, INPUT);
	
	attachInterrupt(RC_INPUT_STR, channel_a_ISR, CHANGE);
	attachInterrupt(RC_INPUT_THR, channel_b_ISR, CHANGE);
    
    ServoSTR.attach(PIN_STR, 1000, 2000); //Clamp values to 1k to 2k.
    ServoTHR.attach(PIN_THR, 1000, 2000);
	
	watchdog.begin(checkDisable, 10000); //Disable after 1/100th second if not updated.
    
    gTheOldRCcommand = NOT_ACTUAL_COMMAND;
    gcarState = STATE_MANUAL;//start of in manual (rc control) mode
}

void checkDisable() {
	if ((micros() - lastUpdated_a > 25000) || (micros() - lastUpdated_b > 25000)) { //.25s
		chan_a = 1500;
		chan_b = 1500;
	}
}

/* Interrupt Service Routines for updating channel timings. */

void channel_a_ISR() {
	int currentMicros = micros();
	lastUpdated_a = currentMicros;
	if (digitalRead(RC_INPUT_STR)) {
		chan_a_start = currentMicros;
	}
	else {
		chan_a = currentMicros - chan_a_start;
	}
}

void channel_b_ISR() {
	int currentMicros = micros();
	lastUpdated_b = currentMicros;
	if (digitalRead(RC_INPUT_THR)) {
		chan_b_start = currentMicros;
	}
	else {
		chan_b = currentMicros - chan_b_start;
	}
}

void sendSerialCommand( commandDataStruct *theDataPtr ){
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

void getSerialCommandIfAvailable( commandDataStruct *theDataPtr ){
    // http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
    int cmd_cnt = 0;
    char cmdBuf[MAX_CMD_BUF];
                
    //Serial.flush();
    if (Serial.available()) {        
        Serial.println("Found serial command");
        byte size = Serial.readBytes(cmdBuf, MAX_CMD_BUF);
        
        if (DEBUG_SERIAL) {
            Serial.write(cmdBuf, size);    //echo what the Pi sent right back to it
        }
            
        // tack on a null byte to the end of the line
        cmdBuf[size] = 0;
    
        // strtok splits a C string into substrings, based on a separator character
        char *command = strtok(cmdBuf, ",");    //  get the first substring

        // loop through the substrings, exiting when the null byte is reached
        //    at the end of each pass strtok gets the next substring
        
        while (command != 0) {        
            switch (cmd_cnt) {
            case CMD_AUTO:
                theDataPtr->command = atoi(command);
                Serial.print("debug command:    ");
                Serial.println(theDataPtr->command);
                break;
            case CMD_STR:
                theDataPtr->str = atoi(command);    
                if( theDataPtr->str > 2000 || theDataPtr->str < 1000 ){
                    theDataPtr->command = STEERING_VALUE_OUT_OF_RANGE;    
                }
                break;
                
            case CMD_THR:
                theDataPtr->thr = atoi(command);    
                if( theDataPtr->thr > 2000 || theDataPtr->thr < 1000 ){
                    theDataPtr->command = THROTTLE_VALUE_OUT_OF_RANGE;    
                }
                break;
                
            case CMD_TIME:
                theDataPtr->time = atoi(command);    
                break;
                
            default:
                if (DEBUG_SERIAL) {
                    Serial.println("Too many values in command");
                }
                theDataPtr->command = TOO_MANY_VALUES_IN_COMMAND;    
            }
            
            // Get the next substring from the input string
            // changing the first argument from cmdBuf to 0 is the strtok method for subsequent calls
            command = strtok(0, ",");
            cmd_cnt++;
        }
    }
    theDataPtr->time = millis();
}


void handleRCSignals( commandDataStruct *theDataPtr ) {
    theDataPtr->time = millis();
    unsigned long STR_VAL = chan_a; // Read pulse width of
    unsigned long THR_VAL = chan_b; // each channel
    if (STR_VAL == 0) {    // no steering RC signal 
        if( gTheOldRCcommand != RC_SIGNAL_WAS_LOST ){    // only print RC message once
            if (DEBUG_SERIAL) {
                Serial.println("RC out of range or powered off\n");
            }
            gTheOldRCcommand = RC_SIGNAL_WAS_LOST;
        }
        theDataPtr->command = RC_SIGNAL_WAS_LOST;
        return;
    }
    // check for reverse ESC signal from RC while in autonomous mode (user wants to stop auto)
    if ( gcarState==STATE_AUTONOMOUS) {    
        if( THR_VAL > throttleThresholdToShutdownAuto ){     // signals increase with reverse throttle movement
            theDataPtr->command = RC_SIGNALED_STOP_AUTONOMOUS;
            return;
        }
    }
    // clip the RC signals to more car appropriate ones

    if( STR_VAL > maximumSteeringValue )
        STR_VAL = maximumSteeringValue;

    else if( STR_VAL < minimumSteeringValue )
        STR_VAL = minimumSteeringValue;

    if( THR_VAL > maximumThrottleValue )
        THR_VAL = maximumThrottleValue;

    else if( THR_VAL < minimumThrottleValue )
        THR_VAL = minimumThrottleValue;

             

    // Create 16 bits values from 8 bits data
    // Accelerometer
    theDataPtr->ax=0;
    theDataPtr->ay=0;
    theDataPtr->az=0;

    // Gyroscope
    theDataPtr->gx=0;
    theDataPtr->gy=0;
    theDataPtr->gz=0;
    
    theDataPtr->thr = (int) THR_VAL;
    theDataPtr->str = (int) STR_VAL;
    theDataPtr->time = millis();
    theDataPtr->command = GOOD_RC_SIGNALS_RECEIVED;
}

int ledcounter=0;
bool ledstate=0;

void loop() {
// ------------------------- Handle RC Commands -------------------------------
    //we create three commandDataStructs, one each for RC and Serial input, and 
    //one for output
    delay(10);
    commandDataStruct RCInputData, SerialInputData, SerialOutputData;
    RCInputData.command=NOT_ACTUAL_COMMAND;
    SerialInputData.command=NOT_ACTUAL_COMMAND;
    SerialOutputData.command=NOT_ACTUAL_COMMAND;
    SerialInputData.thr=0;
    SerialInputData.str=0;
        
    handleRCSignals( &RCInputData );
    getSerialCommandIfAvailable( &SerialInputData );

    //if this variable is true by the end of loop, we send a serial frame
    bool transmitData=false;

    switch (gcarState){
    case STATE_TERM_AUTO: 
        //if we are in this state, we recieved an RC stop signal, and we're waiting
        //for an ack from the pi so we can stop sending the stop command. All we care
        //about is getting the ack, so we don't even need to check the RC input
        if (SerialInputData.command==STOPPED_AUTO_COMMAND_RECEIVED){
            //if we get the ack from the pi, we can return to manual mode
            gcarState=STATE_MANUAL;
        }else{
            //otherwise, send the stop command again
            SerialOutputData.command=RC_SIGNALED_STOP_AUTONOMOUS;
            transmitData=true;
	}
	break;
    case STATE_AUTONOMOUS:
        //Serial.println("AUTONOMOUS MODE");
        //autonomous state-- while in this state, we have to check for stop auto 
        //commands from serial or RC. The only things we check for are RUN_AUTONOMOUSLY
        //and STOP_AUTONOMOUS commands from the Pi, and RC_SIGNALED_STOP_AUTONOMOUS commands
        //from the remote. 
        if (RCInputData.command==RC_SIGNALED_STOP_AUTONOMOUS){ 
            //we could also check for signal_lost signal here, but I don't think that will occur
            SerialOutputData.command=RC_SIGNALED_STOP_AUTONOMOUS;
            SerialOutputData.str = gCenteredSteeringValue;    //  center the steering
	    SerialOutputData.thr = gCenteredThrottleValue;    //  turn off the motor
	    ServoSTR.writeMicroseconds( SerialOutputData.str / 1000);
	    ServoTHR.writeMicroseconds( SerialOutputData.thr / 1000);
            transmitData=true;
            gcarState=STATE_TERM_AUTO;
	}else if(SerialInputData.command==STOP_AUTONOMOUS){
            //we're only sending the ack once, so the Pi might miss it and send more 
            //STOP_AUTO commands. So we have to be sure to check for them in manual state
            //and send more stopped_auto acks
            SerialOutputData.command=STOPPED_AUTO_COMMAND_RECEIVED; 
            SerialOutputData.str = gCenteredSteeringValue;    //  center the steering
	    SerialOutputData.thr = gCenteredThrottleValue;    //  turn off the motor
	    ServoSTR.writeMicroseconds( SerialOutputData.str );
	    ServoTHR.writeMicroseconds( SerialOutputData.thr );
            transmitData=true;
            gcarState=STATE_MANUAL;
        }else if(SerialInputData.command==RUN_AUTONOMOUSLY){
            //we have a new autonomous command -- execute it
            ServoSTR.writeMicroseconds( SerialInputData.str );
	    ServoTHR.writeMicroseconds( SerialInputData.thr );
            SerialOutputData.str = SerialInputData.str;   //put received command in 
	    SerialOutputData.thr = SerialInputData.thr;   //output to echo back
	    SerialOutputData.command = GOOD_PI_COMMAND_RECEIVED; 
            transmitData=true;
	}
        break;
    case STATE_MANUAL:
        Serial.println("MANUAL MODE");
        //manual RC state -- while in this state, we send back data frames with the RC signals
        //we also observe for run_auto commands from the Pi and stop_auto commands from the Pi. 
        //Receiving the latter while we're in manual means the Pi missed the stopped_auto ack, 
        //so we should send another.
        if(SerialInputData.command==RUN_AUTONOMOUSLY){
            ServoSTR.writeMicroseconds( SerialInputData.str );
	    ServoTHR.writeMicroseconds( SerialInputData.thr );
            SerialOutputData.str = SerialInputData.str;   //put received command in 
	    SerialOutputData.thr = SerialInputData.thr;   //output to echo back
	    SerialOutputData.command = GOOD_PI_COMMAND_RECEIVED; 
            transmitData=true;
            gcarState=STATE_AUTONOMOUS;
        }else if(SerialInputData.command==STOP_AUTONOMOUS){
            //it's kind of clumsy to expect to handle this. Really, we should improve the 
            //serial processing on the Pi so that we don't have to worry about commands or 
            //acks being missed. Hopefully this is a temporary solution.
            //The car should respond to RC signals anyway.
            SerialOutputData.command=STOPPED_AUTO_COMMAND_RECEIVED; 
            SerialOutputData.str = RCInputData.str;   
	    SerialOutputData.thr = RCInputData.thr;   
	    ServoSTR.writeMicroseconds( SerialOutputData.str );
	    ServoTHR.writeMicroseconds( SerialOutputData.thr );
            transmitData=true;
	}else if(RCInputData.command==GOOD_RC_SIGNALS_RECEIVED){
            //This is what we want to happen during manual mode.
            SerialOutputData.str = RCInputData.str;   
	    SerialOutputData.thr = RCInputData.thr;   
	    ServoSTR.writeMicroseconds( SerialOutputData.str );
	    ServoTHR.writeMicroseconds( SerialOutputData.thr );
            SerialOutputData.command=GOOD_RC_SIGNALS_RECEIVED;
            transmitData=true;
        }
        break;
    }

    if (transmitData==true){
       SerialOutputData.time=SerialInputData.time; //populate time field
       //in the future, the imu will work. The values to send back will
       // always be the ones recorded in RCInputData
       SerialOutputData.ax=RCInputData.ax;
       SerialOutputData.ay=RCInputData.ay;
       SerialOutputData.az=RCInputData.az;
       SerialOutputData.gx=RCInputData.gx;
       SerialOutputData.gy=RCInputData.gy;
       SerialOutputData.gz=RCInputData.gz;
       sendSerialCommand(&SerialOutputData);
    }
}
