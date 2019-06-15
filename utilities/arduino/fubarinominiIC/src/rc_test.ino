#include <Arduino.h>

#define RC_INPUT_STR_PIN 0	//goes to channel 4
#define RC_INPUT_THR_PIN 10	//goes to channel 2
#define RC_INPUT_KILL_PIN 7 	//goes to channel 5
#define RC_INPUT_EN_PIN 6 	//goes to channel 6

#define RC_INPUT_COUNT 4

volatile uint16_t pulseHighTime[RC_INPUT_COUNT];
volatile uint16_t pulseLowTime[RC_INPUT_COUNT];

inline int pulseRead(int RCindex) {
  return (pulseHighTime[RCindex] > 0) ? (int)(4.0 * pulseHighTime[RCindex] / 3.0) : (int)(4.0 * pulseHighTime[RCindex] / 3.0 + 0xFFFF);
}
//inline int pulseRead(int RCindex){return (int)(0.8*pulseHighTime[RCindex]);}

//interrupt service routine for first input capture module
void __USER_ISR InputCaptureSTR_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;

  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  if (IC1CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_STR_PIN) == HIGH)
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

//interrupt service routine for first input capture module
void __USER_ISR InputCaptureKILL_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;

  clearIntFlag(_INPUT_CAPTURE_2_IRQ);
  if (IC2CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_KILL_PIN) == HIGH)
    {
      risingEdgeTime = IC2BUF;
      pulseLowTime[2] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC2BUF;
      pulseHighTime[2] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

//interrupt service routine for first input capture module
void __USER_ISR InputCaptureEN_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;

  clearIntFlag(_INPUT_CAPTURE_3_IRQ);
  if (IC3CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_EN_PIN) == HIGH)
    {
      risingEdgeTime = IC3BUF;
      pulseLowTime[3] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC3BUF;
      pulseHighTime[3] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

//interrupt service routine for first input capture module
void __USER_ISR InputCaptureTHR_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;

  clearIntFlag(_INPUT_CAPTURE_4_IRQ);
  if (IC4CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_THR_PIN) == HIGH)
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
  //peripheral pin select
  mapPps(RC_INPUT_STR_PIN, PPS_IN_IC1);
  mapPps(RC_INPUT_KILL_PIN, PPS_IN_IC2);
  mapPps(RC_INPUT_EN_PIN, PPS_IN_IC3);
  //mapPps(3, PPS_IN_IC4);
  mapPps(RC_INPUT_THR_PIN, PPS_IN_IC4);

  //setup input capture modules one, two, three and four
  IC1CON = 0;
  IC1CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
  IC1CONbits.ICTMR = 0; // Set to user Timer3
  IC1CONbits.ON = 1;    // Turn IC1 on


  IC2CON = 0;
  IC2CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
  IC2CONbits.ICTMR = 0; // Set to user Timer3
  IC2CONbits.ON = 1;    // Turn IC2 on

  IC3CON = 0;
  IC3CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
  IC3CONbits.ICTMR = 0; // Set to user Timer3
  IC3CONbits.ON = 1;    // Turn IC3 on


  IC4CON = 0;
  IC4CONbits.ICM = 1;   // Capture an interrupt on every rising and falling edge
  IC4CONbits.ICTMR = 0; // Set to user Timer3
  IC4CONbits.ON = 1;    // Turn IC4 on

  /*We're using timer2 for the input capture. This shouldn't interfere with pwm
    output, which uses timers 3-5.
  */
  PR3 = 0xFFFF;         // This tells timer 3 to count up to 0xFFFF, after which it will restart at 0
  T3CONbits.TCKPS = 6;  // 1:64 prescale, which means 48MHz/64 or 0.75MHz clock rate
  T3CONbits.TON = 1;    // Turn on Timer3

  pinMode(RC_INPUT_STR_PIN, INPUT);
  pinMode(RC_INPUT_THR_PIN, INPUT);
  pinMode(RC_INPUT_KILL_PIN, INPUT);
  pinMode(RC_INPUT_EN_PIN, INPUT);
  //pinMode(PIN_LED1, OUTPUT);
  //digitalWrite(PIN_LED1, LOW);

  //these lines set up the interrupt functions to trigger
  setIntVector(_INPUT_CAPTURE_1_VECTOR, InputCaptureSTR_ISR);
  setIntPriority(_INPUT_CAPTURE_1_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  setIntEnable(_INPUT_CAPTURE_1_IRQ);


  setIntVector(_INPUT_CAPTURE_2_VECTOR, InputCaptureKILL_ISR);
  setIntPriority(_INPUT_CAPTURE_2_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_2_IRQ);
  setIntEnable(_INPUT_CAPTURE_2_IRQ);

  setIntVector(_INPUT_CAPTURE_3_VECTOR, InputCaptureEN_ISR);
  setIntPriority(_INPUT_CAPTURE_3_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_3_IRQ);
  setIntEnable(_INPUT_CAPTURE_3_IRQ);
/*
  setIntVector(_INPUT_CAPTURE_4_VECTOR, InputCaptureEN_ISR);
*/
  setIntVector(_INPUT_CAPTURE_4_VECTOR, InputCaptureTHR_ISR);
  setIntPriority(_INPUT_CAPTURE_4_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_4_IRQ);
  setIntEnable(_INPUT_CAPTURE_4_IRQ);


}

void sendSerialLine(int STR, int THR, int KILL, int EN){
  Serial.print(STR);
  Serial.print(",");
  Serial.print(THR);
  Serial.print(",");
  if(KILL>1900){
    Serial.print("KILL");
  }else{
    Serial.print("GO");
  }
  Serial.print(",");
  if(EN>1900){
    Serial.print("RC_ENABLE");
  }else if(EN>1400){
    Serial.print("RC_THROTTLE");
  }else{
    Serial.print("RC_DISABLE");
  }
  Serial.println();
}

void loop(){

  unsigned long STR_VAL=pulseRead(0);
  unsigned long THR_VAL=pulseRead(1);
  unsigned long KILL_VAL=pulseRead(2);
  unsigned long EN_VAL=pulseRead(3);

  sendSerialLine(STR_VAL, THR_VAL, KILL_VAL, EN_VAL);
  //sendSerialLine(STR_VAL, THR_VAL, 0, 0); 
  
  delay(200);

}





