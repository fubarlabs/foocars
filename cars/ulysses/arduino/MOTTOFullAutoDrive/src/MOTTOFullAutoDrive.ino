#include <Arduino.h>
//#include <SoftPWMServo.h>
#include <Servo.h>

#define DEBUG_SERIAL 1
#define MAX_CMD_BUF 17 
#define CMD_AUTO 0
#define CMD_STR 1
#define CMD_THR 2
#define CMD_TIME 3

const int PIN_STR = 9;
const int PIN_THR = 7;
const int PIN_IN_STR = 0;
const int PIN_IN_THR = 10;
const int PIN_AUTO_BTN = 15;

unsigned long last_serial_time;
unsigned long last_time;
boolean BLINK = true;

// shoot through delay
int PREV_DIR = LOW;
const int SHOOT_DELAY = 250;

Servo ServoSTR;
Servo ServoTHR;
void setup() {
  Serial.begin(9600);
  delay(250);

  pinMode(PIN_IN_STR, INPUT);
  pinMode(PIN_IN_THR, INPUT);
  pinMode(PIN_AUTO_BTN, INPUT);
  pinMode(PIN_LED1, OUTPUT);

  digitalWrite(PIN_LED1, LOW);

  ServoSTR.attach(PIN_STR);
  ServoTHR.attach(PIN_THR);

}

/*
   Find and do the autonmous commands
   /*
     read entire input max length
     while more serial
     fill the comdBuf until a ','
     cmds
     Output:
     `accel_x, accel_y, accel_z, yaw, pitch, roll,time`.
     Input Commands:
     Only need steering and throttle

     `auto 0/1, steering 1000-2000, thr amount 1000-2000, timestamp`
     1. steer 1000 - 2000
     2. throttle  1000 - 2000   When new line end
     execute the commands
     OUTPUT the results:
     auto, str, thr, millis, ???
*/
void doAutoCommands() {
  // http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
  int cmd_cnt = 0;
  char cmdBuf[MAX_CMD_BUF + 1];

  int auton;
  int str;
  int thr;
  unsigned int time;

  byte size = Serial.readBytes(cmdBuf, MAX_CMD_BUF);
  cmdBuf[size] = 0;
  char *command = strtok(cmdBuf, ",");
  for(int i=0; i<size; i++){
    Serial.print(cmdBuf[i]);
  }
  //Serial.println();
  //Serial.println(cmdBuf);
  while (command != 0) {
    switch (cmd_cnt) {
    case CMD_AUTO:
      auton = atoi(command);	
      break;
    case CMD_STR:
      str = atoi(command);
      if (str > 2050 || str < 500) {
        return;
      }
      if (DEBUG_SERIAL) {
        //Serial.printf("%d, %d\n", cmd_cnt, str);
      }
      break;
    case CMD_THR:
      thr = atoi(command);
      if (thr > 2000 || thr < 1000) {
        return;
      }
      if (DEBUG_SERIAL) {
        //Serial.printf("%d, %d\n", cmd_cnt, thr);
      }
      break;
    case CMD_TIME:
      time = atoi(command);
        /*
            Remove time check
          if (time < last_time) {
          return;
          }
        */
      last_time = time;
      if (DEBUG_SERIAL) {
          //Serial.printf("%d, %lu\n", cmd_cnt, time);
       }
       break;
    default:
      if (DEBUG_SERIAL) {
        Serial.println("NOOP");
      }
      return; // return if there are too many commands or non matching
    }
    command = strtok(0, ",");
    cmd_cnt++;

    if (cmd_cnt == 4) {
      if (DEBUG_SERIAL) {
        Serial.printf("str: %d, thr: %d, time: %lu\n", str, thr, time);
      }
      // do commands
            //printData(ottoIMU.ax, ottoIMU.ay, ottoIMU.az, ottoIMU.gx, ottoIMU.gy,
      //          ottoIMU.gz, millis(), str, thr);

      ServoSTR.writeMicroseconds(str);
      ServoTHR.writeMicroseconds(thr);
      if (DEBUG_SERIAL) {
	      //Serial.printf("DONE COMMANDS: %lu, %lu\n", str, thr);
      }
    }
  }

  //delay(100);
  
}

void doAction() {

  unsigned long STR_VAL = pulseIn(PIN_IN_STR, HIGH, 25000); // Read pulse width of
  unsigned long THR_VAL = pulseIn(PIN_IN_THR, HIGH, 25000); // each channel

  // check if auto on
  if (digitalRead(PIN_AUTO_BTN) == true) {
    // Turn on when auto
    digitalWrite(PIN_LED1, HIGH);
    if (DEBUG_SERIAL) {
      Serial.println("FULL AUTO");
    }
    // auto mode is on
    // Check if command waiting
    if (Serial.available() > 0) {
      doAutoCommands();
    }
    return;
  } else if (STR_VAL == 0) // if no str data stop
  {                        // Turn off when not in auto
    if (DEBUG_SERIAL) {
      Serial.printf("Out of Range or Powered Off\n");
    } // Turn off when not in auto

    // set brake
    // kill the machine
    // pick a value that stops the car
    Serial.flush();
    ServoSTR.writeMicroseconds(1500);
    ServoTHR.writeMicroseconds(1500);
  } else {

    Serial.flush();
    ServoSTR.writeMicroseconds(STR_VAL);
    ServoTHR.writeMicroseconds(THR_VAL);
    printData(0, 0, 0, 0, 0, 0, millis(), STR_VAL, THR_VAL);
  }
}
/*
   printIMU to serial port
*/
void printData(float ax, float ay, float az, float gx, float gy, float gz,
               unsigned long time, int str, int thr) {
  // Serial.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%lu,%d,%d\n",
  //              ax, ay, az, gx, gy, gz, millis(), str, thr);

  
  Serial.print(ax);
  Serial.print(",");
  Serial.print(ay);
  Serial.print(",");
  Serial.print(az);
  Serial.print(",");
  Serial.print(gx);
  Serial.print(",");
  Serial.print(gy);
  Serial.print(",");
  Serial.print(gz);
  Serial.print(",");
  Serial.print(millis());
  Serial.print(",");
  Serial.print(str);
  Serial.print(",");
  Serial.print(thr);
  Serial.println();
}

void loop() {

  //doAction();

	if (Serial.available() > 0) {
		doAutoCommands();
	}

  //delay(10);
}
