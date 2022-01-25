#include <Servo.h>

// Important explanation of this code
// 
// General: this code allows a servo to turn more than 180 but in a controllable way, how?
// the code first exploits the feature of setting the maximum and minimum microseconds inside servo.attach()
// in order to allow the servo to turn infinitely in a certain direction, it then tricks the servo into
// turning 180 degrees uninterrupted an infinite amount of repetitions without having to reset back to zero
// but the important part is that it shoots the servo turning infinitely and then assumes after a certain 
// period of time that the servo might have made enuff turning to be close to an angle that is known within its
// accurate range so we APPLY that angle in order to stop the servo in a very accurate angle
// why all this? because infinitely turning servos don't stop at the exact same angle everytime even though
// the specified turning time is the same



Servo servo;
#define servoPin 9
int turn_delay = 200;

void setup() {
  Serial.begin(9600);
  //servo.attach(servoPin, 100, 2900);
  servo.attach(servoPin);
}

long double_turn = 1000;
long maxi = 2000;
void loop() {
  
  if(Serial.available()>0){
    String msg = Serial.readStringUntil('\n');

    String command = getValue(msg, ' ', 0);

    // this iif statement is to find the maximum microseconds of a servo before it starts to just go infinitely
    if(command=="SEARCHFORMAX" || command=="sfm" || command=="SFM"){
      long lower;
      lower = getValue(msg, ' ', 1).toInt();
      long upper;
      upper = getValue(msg, ' ', 2).toInt();
      maxi += upper;
      Serial.println("applying min " + String(lower) + " and maxi " + String(maxi));
      servo.attach(servoPin, lower, maxi);
      servo.writeMicroseconds(maxi);
      
    } else if(command=="RESET" || command=="re" || command=="RE"){
      Serial.println("resetting");
      servo.attach(servoPin);
      
    } else if(command=="ANGLE" || command=="A" || command=="a"){
      long angle;
      angle = getValue(msg, ' ', 1).toInt();
      if(!isnan(angle)){
        Serial.println("applying angle " + String(angle));
        servo.write(angle);
      } else {
        Serial.println("angle is not a number " + String(angle));
      }
    } else if(command=="MILLISECONDS" || command=="M" || command=="m"){
      String angleStr = getValue(msg, ' ', 1);
      long angle;
      angle = angleStr.toInt();
        Serial.println(angleStr);
        Serial.println(angle==40000);
      if(!isnan(angle)){
        Serial.println("applying angle " + String(angle));
        servo.writeMicroseconds(angle);
      } else {
        Serial.println("angle is not a number " + String(angle));
      }
    } else if(command=="SEQUENCE" || command=="S" || command=="s"){
      Serial.println("Starting");
      servo.attach(servoPin);
      servo.write(0);
      Serial.println("Servo about to turn after 3 seconds...");
      delay(3000);
      servo.attach(servoPin, 100, 2900);
      servo.writeMicroseconds(100);
      delay(double_turn);
      servo.attach(servoPin);
      servo.write(180);
      Serial.println("Finished");
      
    } else if(command=="UPDATEDOUBLETURNTIME" || command=="UDTT" || command=="udtt"){
      String angleStr = getValue(msg, ' ', 1);
      long angle;
      angle = angleStr.toInt();
        Serial.println(angleStr);
        Serial.println(angle==40000);
      if(!isnan(angle)){
        Serial.println("Updating double turn time to " + String(angle));
        double_turn = angle;
      } else {
        Serial.println("time is not a number " + String(angle));
      }
      
    } else {
      Serial.println("unknown command " + String(command));
    }
  }
}

String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
