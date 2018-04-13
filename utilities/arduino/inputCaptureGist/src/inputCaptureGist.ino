/* Sample RC servo input for 4 channels using Input Capture hardware perihperal and interrupts
 *  Written for Rick Anderson by Brian Schmalz
 *  11/11/2017
 *  This software is put in the public domain. 
 *  This sketch is means for a chipKIT Fubarino SD board, but can be easily adpated to any PIC32 based Arduino compatible board.
 */

/* Fubarino SD can only use pins 0, 1, 2, 3, and 10 as Input Capture.
 * On any chipKIT board with PPS (like Fubarino Mini) additional setup is necessary to map the Input Capture
 * peripherals to speciffic I/O pins, but you have much more flexibility in pin assignments.
 */
#include <Arduino.h>
// Which pins correspond to which RC input channel?
#define RC_INPUT_1 0
#define RC_INPUT_2 1
#define RC_INPUT_3 2
#define RC_INPUT_4 3
// How many RC input channels are there?
#define RC_INPUT_COUNT 4

// These two arrays hold the latest pulse measurements for each RC input channel
volatile uint16_t pulseHighTime[RC_INPUT_COUNT];
volatile uint16_t pulseLowTime[RC_INPUT_COUNT];

/* Four Input Capture Interrupt Service Routines
 *  These functions get called on each rising and falling edge. They check to see
 *  if a rising edge or falling edge just happened, then read out the Timer2 value that
 *  got latched on the edge, and calculate the high and low pulse times, then stick those
 *  times in the proper array.
 */
void __USER_ISR InputCapture1_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  if (IC1CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_1) == HIGH)
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

void __USER_ISR InputCapture2_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_2_IRQ);
  if (IC2CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_2) == HIGH)
    {
      risingEdgeTime = IC2BUF;
      pulseLowTime[1] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC2BUF;
      pulseHighTime[1] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

void __USER_ISR InputCapture3_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_3_IRQ);
  if (IC3CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_3) == HIGH)
    {
      risingEdgeTime = IC3BUF;
      pulseLowTime[2] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC3BUF;
      pulseHighTime[2] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

void __USER_ISR InputCapture4_ISR(void) {
  static uint16_t risingEdgeTime = 0;
  static uint16_t fallingEdgeTime = 0;
  
  clearIntFlag(_INPUT_CAPTURE_4_IRQ);
  if (IC4CONbits.ICBNE == 1)
  {
    if (digitalRead(RC_INPUT_4) == HIGH)
    {
      risingEdgeTime = IC4BUF;
      pulseLowTime[3] = risingEdgeTime - fallingEdgeTime;
    }
    else
    {
      fallingEdgeTime = IC4BUF;
      pulseHighTime[3] = fallingEdgeTime - risingEdgeTime;
    }
  }
}

void setup() {
  Serial.begin(9600);
  delay(3000);
  Serial.println("OK we are starting now");

  /* Set up each of the four Input Capture modules 
   * We want them to generate an interrupt on each rising and falling edge of the input
   * We also want them all to use Timer2 as their timebase timer
   */
  IC1CON = 0;
  IC1CONbits.ICM = 1;   // Captured and interrupt on every rising and falling edge
  IC1CONbits.ICTMR = 1; // Set to user Timer2
  IC1CONbits.ON = 1;    // Turn IC1 on

  IC2CON = 0;
  IC2CONbits.ICM = 1;   // Captured and interrupt on every rising and falling edge
  IC2CONbits.ICTMR = 1; // Set to user Timer2
  IC2CONbits.ON = 1;    // Turn IC2 on

  IC3CON = 0;
  IC3CONbits.ICM = 1;   // Captured and interrupt on every rising and falling edge
  IC3CONbits.ICTMR = 1; // Set to user Timer2
  IC3CONbits.ON = 1;    // Turn IC3 on

  IC4CON = 0;
  IC4CONbits.ICM = 1;   // Captured and interrupt on every rising and falling edge
  IC4CONbits.ICTMR = 1; // Set to user Timer2
  IC4CONbits.ON = 1;    // Turn IC4 on

  /* Set up Timer2: We want it to simply count up. We set the prescaler to 1:64
   *  so that the 80MHz PCLK gets divided down to 1.25Mhz. This is nice because
   *  then it gives us both high and low periods under 65535 for normal RC servo
   *  times (0-3 ms high time and 17-20ms low time)
   */
  PR2 = 0xFFFF;         // Run from 0 to 0xFFFF
  T2CONbits.TCKPS = 6;  // 1:64 prescale, which means 80MHz/64 or 1.25MHz clock rate
  T2CONbits.TON = 1;    // Turn on Timer2

  // Set all input captures as inputs
  pinMode(RC_INPUT_1, INPUT);
  pinMode(RC_INPUT_2, INPUT);
  pinMode(RC_INPUT_3, INPUT);
  pinMode(RC_INPUT_4, INPUT);
  Serial.println("ready");

  // Set each Input Capture up to use its ISR routine
  setIntVector(_INPUT_CAPTURE_1_VECTOR, InputCapture1_ISR);
  setIntPriority(_INPUT_CAPTURE_1_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_1_IRQ);
  setIntEnable(_INPUT_CAPTURE_1_IRQ);

  setIntVector(_INPUT_CAPTURE_2_VECTOR, InputCapture2_ISR);
  setIntPriority(_INPUT_CAPTURE_2_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_2_IRQ);
  setIntEnable(_INPUT_CAPTURE_2_IRQ);

  setIntVector(_INPUT_CAPTURE_3_VECTOR, InputCapture3_ISR);
  setIntPriority(_INPUT_CAPTURE_3_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_3_IRQ);
  setIntEnable(_INPUT_CAPTURE_3_IRQ);

  setIntVector(_INPUT_CAPTURE_4_VECTOR, InputCapture4_ISR);
  setIntPriority(_INPUT_CAPTURE_4_VECTOR, 4, 0);
  clearIntFlag(_INPUT_CAPTURE_4_IRQ);
  setIntEnable(_INPUT_CAPTURE_4_IRQ);
}

void loop() {
  static uint32_t lastPrintTime = 0;
  float uSscale = 0.8;
  
  /* So the way things work, the ISRs will get called and they will constantly update
   *  the pulseHighTime and pulseLowTime arrays "in the background". In other words the
   *  mainline code here doesn't ever have to do anything other than simply read out
   *  the values in the arrays, and those values will always be the most recent pulse
   *  measurements. If you care about converting the values to real time (like in 
   *  microsconds), the units for these values are in 1.25MHz 'counts'. So 1ms = 1250
   *  'counts'.
   */
  // To demo things, simply print out all 4 high and low pulse times every half second

  /*In case of clock buffer reset during either pulse high or pulse low, the value of 
    pulseHighTime or pulseLowTime will be negative. If that's the case, just add 0xFFFF 
    (the value the timer counts to) to the value to get the correct duration. 
  */
  for(int i=0; i<4; ++i){
    if(pulseHighTime[i]<0){
      pulseHighTime[i]=pulseHighTime[i]+0xFFFF;
    }
    if(pulseLowTime[i]<0){
      pulseLowTime[i]=pulseLowTime[i]+0xFFFF;
    }
  }

  if ((millis() - lastPrintTime) > 500)
  {
    lastPrintTime = millis();
    char pulses[100];
    char micros[100];
    sprintf(pulses, "high1: %05u low1: %05u high2: %05u low2: %05u high3: %05u low3: %05u high4: %05u low4: %05u\n",
      pulseHighTime[0],
      pulseLowTime[0],
      pulseHighTime[1],
      pulseLowTime[1],
      pulseHighTime[2],
      pulseLowTime[2],
      pulseHighTime[3],
      pulseLowTime[3]
    );
    Serial.print(pulses);
    sprintf(micros, "ch1: %05u ch2: %05u ch3: %05u ch4: %05u\n",    
      (int) (pulseHighTime[0] * uSscale),
      (int) (pulseHighTime[1] * uSscale),
      (int) (pulseHighTime[2] * uSscale),
      (int) (pulseHighTime[3] * uSscale)
    );

    Serial.print(micros); 
  }
}
