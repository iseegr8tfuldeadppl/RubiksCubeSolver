#include <Stepper.h> 
#define STEPS 200

int Speed=600;
Stepper stepper(STEPS, 5, 6); // Pin 3 DIRECTION & Pin 4 STEP Pin of Driver
long value;

void setup() {
  Serial.begin(9600);
  stepper.setSpeed(Speed);
  pinMode(7, OUTPUT);

  digitalWrite(7, HIGH);
}

void loop() {
  if(Serial.available()){
    String msg = Serial.readStringUntil('\n');

    value = msg.toInt();

    Serial.println("Finna apply " + String(value));
    stepper.step(value);
  }

  
}
