#include <Arduino.h>


#include <Servo.h>

#define DEBUG_SERIAL 1
//These lines are for the input capture for pwm read off RC
#define RC_INPUT_STR 0
#define RC_INPUT_THR 10 
#define RC_INPUT_COUNT 2

#define CLIP_THR_VAL_MAX 1605
#define CLIP_THR_VAL_MIN 1305

volatile uint16_t pulseHighTime[RC_INPUT_COUNT];
volatile uint16_t pulseLowTime[RC_INPUT_COUNT];

const int PIN_STR = 9;
const int PIN_THR = 7;

unsigned long steer_history[20]; //Array to store 1/5 of a second of steer values

int steer_next_ind; //index of next value to be written in steer_history

unsigned long thr_zero_val=1498;


//volatile bool staleData=0;

//uint16_t timeoutDelay=0xEFFF; //works out to about 45ms 


Servo ServoSTR;
Servo ServoTHR;

//This function pulls the data being populated by the input capture interrupts.
//it corrects for the timer restarting.
//inline int pulseRead(int RCindex){return (pulseHighTime[RCindex]>=0)?(int)(0.8*pulseHighTime[RCindex]):(int)(0.8*pulseHighTime[RCindex]+0xFFFF);}
inline int pulseRead(int RCindex){return (int)(0.8*pulseHighTime[RCindex]);}
//interrupt service routine for first input capture module
void __USER_ISR InputCaptureSTR_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  if (IC1CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_STR) == HIGH)
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
  //staleData=0;
  //PR2 = IC1BUF+timeoutDelay;
}

//interrupt service routine for second input capture module
void __USER_ISR InputCaptureTHR_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_5_IRQ);
  if (IC5CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_THR) == HIGH)
    {
      risingEdgeTime = IC5BUF;
      pulseLowTime[1] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC5BUF;
      pulseHighTime[1] = fallingEdgeTime - risingEdgeTime;
    }
  }
  //staleData=0;
  //PR2 = IC4BUF+timeoutDelay;
}



/*
void __USER_ISR Timer2_ISR(void){
  clearIntFlag(_TIMER_2_IRQ); //clear interrupt flag in software
  staleData=1; //if we reach the value of PR, then the input capture ISRs 
    //haven't been called for at least timeoutDelay clock cycles. 
  PR2=0xFFFF; //set PR to max value. In this case, the timer will just count 
    //up to max value repeatedly until one of the other ISRs is called and 
    //sets it to timer value incremented by timeoutDelay.
}
*/

unsigned long compAvg(unsigned long *data_array, int len){
    unsigned long result=0;
    for(int i=0; i<len; i++){
        result+=data_array[i];
    }
    return (result/len);
}

void setup()
{
  Serial.begin(9600);
  delay(250);

  //setup input capture modules one and two

  IC1CON = 0;
  IC1CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
  IC1CONbits.ICTMR = 1; // Set to user Timer2
  IC1CONbits.ON = 1;    // Turn IC1 on

  IC5CON = 0;
  IC5CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
  IC5CONbits.ICTMR = 1; // Set to user Timer2
  IC5CONbits.ON = 1;    // Turn IC2 on


  /*We're using timer2 for the input capture. This shouldn't interfere with pwm
    output, which uses timers 3-5.
  PR2 = timeoutDelay;         
  */ 
  PR2 = 0xFFFF;
  T2CONbits.TCKPS = 6;  // 1:64 prescale, which means 80MHz/64 or 1.25MHz clock rate
  T2CONbits.TON = 1;    // Turn on Timer2
  


  pinMode(RC_INPUT_STR, INPUT);
  pinMode(RC_INPUT_THR, INPUT);


  //these lines set up the interrupt functions to trigger 
  setIntVector(_INPUT_CAPTURE_1_VECTOR, InputCaptureSTR_ISR);
  setIntPriority(_INPUT_CAPTURE_1_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  setIntEnable(_INPUT_CAPTURE_1_IRQ);

  setIntVector(_INPUT_CAPTURE_5_VECTOR, InputCaptureTHR_ISR);
  setIntPriority(_INPUT_CAPTURE_5_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_5_IRQ);
  setIntEnable(_INPUT_CAPTURE_5_IRQ);

/*

  setIntVector(_TIMER_2_VECTOR, Timer2_ISR);
  setIntPriority(_TIMER_2_VECTOR, 3, 0); //lower priority than input capture 
  clearIntFlag(_TIMER_2_IRQ);
  setIntEnable(_TIMER_2_IRQ);
*/

  ServoSTR.attach(PIN_STR);
  ServoTHR.attach(PIN_THR);

  for(int i=0; i<20; i++){
    steer_history[i]=1500;
  }
  steer_next_ind=0;
  //thr_zero_val = pulseRead(1);
  
}

void printData(float ax, float ay, float az, float gx, float gy, float gz, unsigned long time, int str, int thr )
{

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


void loop()
{
  delay(20);
  //if(!staleData){ //staleData is false, that means the timer has never reached timeout value
    unsigned long STR_VAL = pulseRead(0); // Read the pulse width of
    unsigned long THR_VAL = pulseRead(1); // each channel
    //unsigned long STR_VAL = pulseIn(RC_INPUT_STR, HIGH, 25000);
    //unsigned long THR_VAL = pulseIn(RC_INPUT_THR, HIGH, 25000);

    long thr_dif=long(THR_VAL)-long(thr_zero_val);
    steer_history[steer_next_ind]=STR_VAL;
    steer_next_ind=(steer_next_ind+1)%20;
    unsigned long FILT_STR_VAL=compAvg(steer_history, 20);

    ServoSTR.writeMicroseconds(FILT_STR_VAL);
    unsigned long CLIP_THR_VAL; 
  /*  if(thr_dif>50){
      CLIP_THR_VAL = CLIP_T_VAL;
    }else if(thr_dif<-50){
      CLIP_THR_VAL=1350;
    }else{
      CLIP_THR_VAL=thr_zero_val;
    }
*/
  if(THR_VAL > CLIP_THR_VAL_MAX) {
    CLIP_THR_VAL = CLIP_THR_VAL_MAX;
  }
  else if (THR_VAL <  CLIP_THR_VAL_MIN ) {  
    CLIP_THR_VAL = CLIP_THR_VAL_MIN;
  } else {
    CLIP_THR_VAL = THR_VAL;
  }  

    ServoTHR.writeMicroseconds(CLIP_THR_VAL);
    printData(0, 0, 0, 0, 0, 0, millis(), FILT_STR_VAL, CLIP_THR_VAL);
/*
  }else{
    Serial.println("no new PWM value");
    ServoTHR.writeMicroseconds(thr_zero_val);
    ServoSTR.writeMicroseconds(1500);
  }
*/
}
