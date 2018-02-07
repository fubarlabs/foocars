#include <Arduino.h>

byte Pins[] = {A11, A12, A13, A14, 27, 26, 25, 24};



int timer = 500;           // The higher the number, the slower the timing.

void setup() {
  for (int x = 0; x < 8; x++)
    pinMode( Pins[x], OUTPUT);

}

void dispBinary(byte n)
{
    for (byte i=0; i<8; i++) {
        digitalWrite( Pins[i], n & 1);
        n /= 2;
    }
}

void loop() {
    

  for (int x = 0; x < 256; x++)
  {
    dispBinary( x );
    delay(timer);
   }

}
