#include <Servo.h>
Servo ServoInfiniteSpin; 
Servo ServoSendTo90Degrees; 

void setup() {
  ServoInfiniteSpin.attach(9);
  ServoSendTo90Degrees.attach(6);
}

void loop() {

  // send to 90degrees on pin 6
  ServoSendTo90Degrees.write(90);
  
  // infinite spin on pin 9
  ServoInfiniteSpin.write(180); //clockwise rotation 
  delay(2000); //rotation duration in ms 
  ServoInfiniteSpin.detach(); //detach servo to prevent “creeping” effect 
  delay(500); //short pause 
  ServoInfiniteSpin.attach(9); //reattach servo to pin 9 
  ServoInfiniteSpin.write(0); //counterclockwise rotation 
  delay(2000); //rotation duration in ms 
  ServoInfiniteSpin.detach(); //detach servo to prevent “creeping” effect 
  delay(500); //short pause 
  ServoInfiniteSpin.attach(9); //reattach servo to pin 9 before looping 

}
