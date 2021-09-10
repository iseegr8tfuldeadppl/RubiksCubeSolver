#include <Stepper.h> 
#define STEPS 200
#include <ctype.h>

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver

Stepper stepper(STEPS, 3, 4); // Pin 2 connected to DIRECTION & Pin 3 connected to STEP Pin of Driver
// activator = pin 11

void setup() {
  Serial.begin(9600);
  stepper.setSpeed(500); // max 1000
}


void loop() {
  
  if (Serial.available() > 0) {
    
    // Step 1: read the incoming message:
    char received = Serial.read();

    switch(received){
      case 'r':
        Serial.println("Run");
        delay(2000);
        stepper.step(200);
        break;
    }
  }
}
