#include <Servo.h>

Servo servo;

void setup() {
  servo.attach(5, 100, 2400);
}

void loop() {
  servo.write(0);
  delay(2000);
  servo.write(180);
  delay(2000);
  servo.write(90);
  delay(2000);
}
