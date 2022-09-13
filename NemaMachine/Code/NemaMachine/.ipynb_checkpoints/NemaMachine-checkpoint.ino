#include <Stepper.h> 
#define STEPS 200

long value;
int Speed=500;
Stepper stepper(STEPS, 3, 4); // Pin 3 DIRECTION & Pin 4 STEP Pin of Driver

#define StepperSleepo 6

void setup() {
  
  Serial.begin(9600);
  stepper.setSpeed(Speed); // max 1000
  
  pinMode(StepperSleepo, OUTPUT);
  digitalWrite(StepperSleepo, LOW);
  
  Serial.println("Speed " + String(Speed));
  Serial.println("Ready");
}

void loop() {
  detectCommand();
}

void detectCommand(){
  if (Serial.available() > 0) {
    String request = Serial.readStringUntil('\n');
    processCommand(request);
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


void processCommand(String request){
  String command = getValue(request, ' ', 0);
  
  if(command=="MOVE"){
    String str = getValue(request, ' ', 1);
    value = str.toInt();
    if(isnan(value)) {
      Serial.println("Nope, invalid steps " + String(value));
      return;
    } else {
      digitalWrite(StepperSleepo, HIGH);
      stepper.step(value);
      digitalWrite(StepperSleepo, LOW);
      Serial.println("Ok, moving stepper by " + String(value));
      return;
    }
  } else if(command="SPEED"){
    String str = getValue(request, ' ', 1);
    value = str.toInt();
    if(isnan(value)) {
      Serial.println("Nope, invalid speed " + String(value));
      return;
    } else {
      Speed = value;
      stepper.setSpeed(Speed);
      Serial.println("Ok, setting speed to " + String(value));
      return;
    }
  }

  Serial.println("Nope, unrecognized command " + String(command) + " with request " + String(request));
}
