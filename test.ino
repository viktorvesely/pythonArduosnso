// Arduino gyroskop a akcelerometr 1

// připojení knihovny Wire
#include <Wire.h>
#include <string.h>
// inicializace proměnné pro určení adresy senzoru
// 0x68 nebo 0x69, dle připojení AD0
const int MPU_addr=0x68;
// inicializace proměnných, do kterých se uloží data
int16_t lastAcX,lastAcY,lastAcZ,lastGyX,lastGyY,lastGyZ;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

void setup()
{
  // komunikace přes I2C sběrnici
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  // komunikace přes sériovou linku rychlostí 115200 baud
  Serial.begin(115200);
}


String padded(int16_t number, int padded) {
    String value = String(number);
    int diff = padded - value.length();
    
    String minus;

    if (number < 0) {
      minus = String("-");
      value = value.substring(1, value.length());
    } else {
      minus = String("");
    }

    if (diff > 0) {
      for (int i = 0; i < diff; i++) {
        value = "0" + value;
      }
    }

    return minus + value + " ";
}

void loop()
{
  // zapnutí přenosu
  Wire.beginTransmission(MPU_addr);
  // zápis do registru ACCEL_XOUT_H
  Wire.write(0x3B);
  Wire.endTransmission(false);
  // vyzvednutí dat z 14 registrů
  Wire.requestFrom(MPU_addr,14,true);
  AcX=Wire.read()<<8|Wire.read();    
  AcY=Wire.read()<<8|Wire.read();
  AcZ=Wire.read()<<8|Wire.read();
  Tmp=Wire.read()<<8|Wire.read();
  GyX=Wire.read()<<8|Wire.read();
  GyY=Wire.read()<<8|Wire.read();
  GyZ=Wire.read()<<8|Wire.read();

  Serial.println(String(AcX) + "," + String(AcY) + "," + String(AcZ) + "," + String(GyX) + "," + String(GyY) + "," + String(GyZ));

  lastAcX=AcX;
  lastAcY=AcY;
  lastAcZ=AcZ;
  lastGyX=GyX;
  lastGyY=GyY;
  lastGyZ=GyZ;

  // delay(50);
}