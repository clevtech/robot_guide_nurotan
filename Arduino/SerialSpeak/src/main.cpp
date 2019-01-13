#include <Arduino.h>


void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
}

void loop()
{
  int incomingByte = '1';
  while(!Serial.available() ){
    delay(10);
    }
  if (Serial.available() > 0) {
                incomingByte = Serial.read();
                if(int(incomingByte) - 48 == 3){
                  Serial.println(1);
                  }

        }
}
