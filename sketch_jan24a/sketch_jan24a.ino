#include <Servo.h>

Servo servo;

void setup() {
  Serial.begin(9600);
  servo.attach(9, 100, 2900);
}

void loop() {
  servo.write(180);
  delay(600);
  servo.write(90);
  delay(2000);
}
