#include <Arduino.h>
#include <Wire.h>

//Test Routine Program - By Stezipoo

//#include <SoftPWMServo.h>
#include <Servo.h>

#define DEBUG_SERIAL 1

// IMU Define
#define    MPU9250_ADDRESS            0x68
#define    MAG_ADDRESS                0x0C

#define    GYRO_FULL_SCALE_250_DPS    0x00  
#define    GYRO_FULL_SCALE_500_DPS    0x08
#define    GYRO_FULL_SCALE_1000_DPS   0x10
#define    GYRO_FULL_SCALE_2000_DPS   0x18

#define    ACC_FULL_SCALE_2_G        0x00  
#define    ACC_FULL_SCALE_4_G        0x08
#define    ACC_FULL_SCALE_8_G        0x10
#define    ACC_FULL_SCALE_16_G       0x18




const int PIN_STR = 9;
const int PIN_THR = 7;
const int PIN_IN_STR = 13;
const int PIN_IN_THR = 12;

unsigned long steer_history[20]; //Array to store 1/5 of a second of steer values

int steer_next_ind; //index of next value to be written in steer_history

unsigned long thr_zero_val;

Servo ServoSTR;
Servo ServoTHR;

//imu unit object
// imu unit object
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




unsigned long compAvg(unsigned long *data_array, int len){
    unsigned long result=0;
    for(int i=0; i<len; i++){
        result+=data_array[i];
    }
    return (result/len);
}

void setup()
{
  Wire.begin();
  Serial.begin(9600);
  delay(250);

  pinMode(PIN_IN_STR, INPUT);
  pinMode(PIN_IN_THR, INPUT);

  //pinMode(PIN_STR, OUTPUT);
  //pinMode(PIN_THR, OUTPUT);
  ServoSTR.attach(PIN_STR);
  ServoTHR.attach(PIN_THR);

  // initIMU
  // Configure gyroscope range
  I2CwriteByte(MPU9250_ADDRESS,27,GYRO_FULL_SCALE_2000_DPS);
  // Configure accelerometers range
  I2CwriteByte(MPU9250_ADDRESS,28,ACC_FULL_SCALE_16_G);
  // Set by pass mode for the magnetometers
  I2CwriteByte(MPU9250_ADDRESS,0x37,0x02);

  // Request first magnetometer single measurement
  I2CwriteByte(MAG_ADDRESS,0x0A,0x01);


  for(int i=0; i<20; i++){
    steer_history[i]=1430;
  }
  steer_next_ind=0;
  thr_zero_val = pulseIn(PIN_IN_THR, HIGH, 25000);
  
}

void printData(unsigned long time, int str, int thr) {
  // Serial.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%lu,%d,%d\n",
  //              ax, ay, az, gx, gy, gz, millis(), str, thr);

  // Read accelerometer and gyroscope
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
  // :::  Magnetometer ::: 


  // Read register Status 1 and wait for the DRDY: Data Ready

  uint8_t ST1;
  do
  {
    I2Cread(MAG_ADDRESS,0x02,1,&ST1);
  }
  while (!(ST1&0x01));

 // Read magnetometer data  
  uint8_t Mag[7];
  I2Cread(MAG_ADDRESS,0x03,7,Mag);


  // Create 16 bits values from 8 bits data

  // Magnetometer
  int16_t mx=-(Mag[3]<<8 | Mag[2]);
  int16_t my=-(Mag[1]<<8 | Mag[0]);
  int16_t mz=-(Mag[5]<<8 | Mag[4]);


}

/*
   printIMU to serial port
*/
void printData(float ax, float ay, float az, float gx, float gy, float gz, unsigned long time, int str, int thr )
{

 // Serial.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%lu,%d,%d\n",
 //               ax, ay,  az, gx, gy, gz, millis(), str, thr);
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
  unsigned long STR_VAL = pulseIn(PIN_IN_STR, HIGH, 25000); // Read the pulse width of
  unsigned long THR_VAL = pulseIn(PIN_IN_THR, HIGH, 25000); // each channel

  long thr_dif=long(THR_VAL)-long(thr_zero_val);
  //try to average the steering values to smooth behavior:
  steer_history[steer_next_ind]=STR_VAL;
  steer_next_ind=(steer_next_ind+1)%20;
  unsigned long FILT_STR_VAL=compAvg(steer_history, 20);

  //SoftPWMServoServoWrite(PIN_STR, STR_VAL);
  ServoSTR.writeMicroseconds(FILT_STR_VAL);
 
  if(thr_dif>50){
    ServoTHR.writeMicroseconds(1570);
  }else if(thr_dif<-50){
    ServoTHR.writeMicroseconds(1400);
  }else{
    ServoTHR.writeMicroseconds(thr_zero_val);
  }


//  ottoIMU.readAccelData(ottoIMU.accelCount);  // Read the x/y/z adc values
//  ottoIMU.getAres();
//  ottoIMU.ax = (float)ottoIMU.accelCount[0] * ottoIMU.aRes; // - accelBias[0];
//  ottoIMU.ay = (float)ottoIMU.accelCount[1] * ottoIMU.aRes; //   accelBias[1];
//  ottoIMU.az = (float)ottoIMU.accelCount[2] * ottoIMU.aRes; // - accelBias[2];
//  ottoIMU.readGyroData(ottoIMU.gyroCount);  // Read the x/y/z adc values
//  ottoIMU.getGres();
//  ottoIMU.gx = (float)ottoIMU.gyroCount[0] * ottoIMU.gRes;
//  ottoIMU.gy = (float)ottoIMU.gyroCount[1] * ottoIMU.gRes;
//  ottoIMU.gz = (float)ottoIMU.gyroCount[2] * ottoIMU.gRes;

  // Serial.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%lu,%d,%d\n", ottoIMU.ax, ottoIMU.ay,  ottoIMU.az, ottoIMU.gx, ottoIMU.gy, ottoIMU.gz, millis(),


  printData(millis(), FILT_STR_VAL, THR_VAL);
  delay(10);
}
