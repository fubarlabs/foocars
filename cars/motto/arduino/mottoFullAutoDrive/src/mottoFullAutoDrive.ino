#include <Arduino.h>

//#include <SoftPWMServo.h>
#include <Servo.h>

#define DEBUG_SERIAL 1

#define MAX_CMD_BUF 17 
#define CMD_AUTO 0
#define CMD_STR 1
#define CMD_THR 2
#define CMD_TIME 3


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

const int PIN_STR = 9;
const int PIN_THR = 7;

int gTotalNumberOfPassesForCommandDisplay = 10000;
int gCountOfPassesForCommandDisplay = gTotalNumberOfPassesForCommandDisplay;

boolean gWantsLEDon;

unsigned long gCenteredSteeringValue;
unsigned long gCenteredThrottleValue;

boolean gIsInAutonomousMode;
int gTheOldRCcommand;
int gTheOldPiCommand;

//these values will be car specific
const unsigned long minimumSteeringValue = 1100;
const unsigned long maximumSteeringValue = 1700;
const unsigned long minimumThrottleValue = 1250;
const unsigned long maximumThrottleValue = 1650;
const unsigned long throttleThresholdToShutdownAuto = 1600;

Servo ServoSTR;
Servo ServoTHR;

//These lines are for the input capture for pwm read off RC
#define RC_INPUT_STR 3
#define RC_INPUT_THR 0
#define RC_INPUT_COUNT 2
volatile uint16_t pulseHighTime[RC_INPUT_COUNT];
volatile uint16_t pulseLowTime[RC_INPUT_COUNT];

//This function pulls the data being populated by the input capture interrupts.
//it corrects for the timer restarting.
inline int pulseRead(int RCindex){return (pulseHighTime[RCindex]>0)?(int)(0.8*pulseHighTime[RCindex]):(int)(0.8*pulseHighTime[RCindex]+0xFFFF);}
//inline int pulseRead(int RCindex){return (int)(0.8*pulseHighTime[RCindex]);}

//interrupt service routine for first input capture module
void __USER_ISR InputCaptureTHR_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  if (IC1CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_THR) == HIGH)
    {
      risingEdgeTime = IC1BUF;
      pulseLowTime[0] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC1BUF;
      pulseHighTime[0] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

//interrupt service routine for second input capture module
void __USER_ISR InputCaptureSTR_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_4_IRQ);
  if (IC4CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_STR) == HIGH)
    {
      risingEdgeTime = IC4BUF;
      pulseLowTime[1] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC4BUF;
      pulseHighTime[1] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

void setup() {
    
    Serial.begin(9600);
    
    Serial.println( "Starting up..." );

        //setup input capture modules one and two
    IC1CON = 0;
    IC1CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
    IC1CONbits.ICTMR = 1; // Set to user Timer2
    IC1CONbits.ON = 1;    // Turn IC1 on

    IC4CON = 0;
    IC4CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
    IC4CONbits.ICTMR = 1; // Set to user Timer2
    IC4CONbits.ON = 1;    // Turn IC2 on

        /*We're using timer2 for the input capture. This shouldn't interfere with pwm
          output, which uses timers 3-5.
        */
    PR2 = 0xFFFF;         // This tells timer 2 to count up to 0xFFFF, after which it will restart at 0
    T2CONbits.TCKPS = 6;  // 1:64 prescale, which means 80MHz/64 or 1.25MHz clock rate
    T2CONbits.TON = 1;    // Turn on Timer2

    pinMode(RC_INPUT_STR, INPUT);
    pinMode(RC_INPUT_THR, INPUT);

        //these lines set up the interrupt functions to trigger 
    setIntVector(_INPUT_CAPTURE_1_VECTOR, InputCaptureTHR_ISR);
    setIntPriority(_INPUT_CAPTURE_1_VECTOR, 4, 0);
    clearIntFlag(_INPUT_CAPTURE_1_IRQ);
    setIntEnable(_INPUT_CAPTURE_1_IRQ);

    setIntVector(_INPUT_CAPTURE_4_VECTOR, InputCaptureSTR_ISR);
    setIntPriority(_INPUT_CAPTURE_4_VECTOR, 4, 0);
    clearIntFlag(_INPUT_CAPTURE_4_IRQ);
    setIntEnable(_INPUT_CAPTURE_4_IRQ);
    
    ServoSTR.attach(PIN_STR);
    ServoTHR.attach(PIN_THR);
    
    gCenteredSteeringValue = 1500;
    gCenteredThrottleValue = 1500;
    
    gTheOldRCcommand = NOT_ACTUAL_COMMAND;
    gIsInAutonomousMode = false;     
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
//    Serial.flush();        // Serial.flush halts program until all characters are sent
}

void getSerialCommandIfAvailable( commandDataStruct *theDataPtr ){
    // http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
    int cmd_cnt = 0;
    char cmdBuf[MAX_CMD_BUF];
                
    if (Serial.available()) {        
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
        
    //else{
    //    theDataPtr->command = NO_COMMAND_AVAILABLE;
    //}
}

void handleRCSignals( commandDataStruct *theDataPtr ) {
    
    unsigned long STR_VAL = pulseRead(RC_INPUT_STR-2); // Read pulse width of
    unsigned long THR_VAL = pulseRead(RC_INPUT_THR); // each channel
    if (STR_VAL == 0) {    // no steering RC signal 
        if( gTheOldRCcommand != RC_SIGNAL_WAS_LOST ){    // only print RC message once
            if (DEBUG_SERIAL) {
                Serial.println("RC out of range or powered off\n");
            }
            gTheOldRCcommand = RC_SIGNAL_WAS_LOST;
        }
        theDataPtr->command = RC_SIGNAL_WAS_LOST;
        return;
    }else if(STR_VAL>2000 or STR_VAL<1000){
        theDataPtr->command = STEERING_VALUE_OUT_OF_RANGE;
        return;
    }
    // check for reverse ESC signal from RC while in autonomous mode (user wants to stop auto)
    if ( gIsInAutonomousMode ) {    
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

void loop() {
// ------------------------- Handle RC Commands -------------------------------
    commandDataStruct theCommandData;
        
    handleRCSignals( &theCommandData );
        
    //    The signal for stopping autonomous driving is user putting car in reverse
    //       this can be a normal operation in manual driving, so a test for auto mode is made

    if(( theCommandData.command == RC_SIGNALED_STOP_AUTONOMOUS ) || ( theCommandData.command == RC_SIGNAL_WAS_LOST )){
        theCommandData.str = gCenteredSteeringValue;    //  center the steering
        theCommandData.thr = gCenteredThrottleValue;    //  turn off the motor
        ServoSTR.writeMicroseconds( theCommandData.str );
        ServoTHR.writeMicroseconds( theCommandData.thr );

        if( gIsInAutonomousMode ){    // send the command to pi to stop autonomous
//            if (DEBUG_SERIAL) {
//                Serial.println("Received RC stop while Autonomous mode is on ");
//            }        
                
            theCommandData.command = STOP_AUTONOMOUS;
            delay( 100 );
            for( int i = 0; i < 5; i++ ){	// fire off 5 stop auto commands
		delay( 100 );
                sendSerialCommand( &theCommandData );
	    }
            gIsInAutonomousMode = false;
        }
    }
    
    delay( 10 );

// ------------------------- Handle Pi Commands -------------------------------
    getSerialCommandIfAvailable( &theCommandData );
            
    if( theCommandData.command == RUN_AUTONOMOUSLY ){
        ServoSTR.writeMicroseconds( theCommandData.str );
        ServoTHR.writeMicroseconds( theCommandData.thr );
        theCommandData.command = GOOD_PI_COMMAND_RECEIVED;
	sendSerialCommand( &theCommandData );
        gIsInAutonomousMode = true;
    }
    
    else if( theCommandData.command == STOP_AUTONOMOUS ){
        theCommandData.str = gCenteredSteeringValue;    //  center the steering
        theCommandData.thr = gCenteredThrottleValue;    //  turn off the motor
        theCommandData.command = STOPPED_AUTO_COMMAND_RECEIVED;
        ServoSTR.writeMicroseconds( theCommandData.str );
        ServoTHR.writeMicroseconds( theCommandData.thr );
	sendSerialCommand( &theCommandData );
        gIsInAutonomousMode = false;
    }
    else if( theCommandData.command == GOOD_RC_SIGNALS_RECEIVED ){
	if( gIsInAutonomousMode == false ){	
            sendSerialCommand( &theCommandData );
	    //    If not in auto mode, send RC values to servo and ESC
	    ServoSTR.writeMicroseconds( theCommandData.str );
	    ServoTHR.writeMicroseconds( theCommandData.thr );
	}
    } 
    else{    // either no command or a bad command was received
        sendSerialCommand( &theCommandData );
    }

}
