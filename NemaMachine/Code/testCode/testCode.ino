#include <Stepper.h> 
#include <EEPROM.h>

// PowerSupply
#define powerSupplyRelayPin A2

// INIT: Stepper variables
// PINOUTS
#define Stepper1Dir 2
#define Stepper1Step 3
#define Stepper1En 4

#define Stepper2Dir 5
#define Stepper2Step 6
#define Stepper2En 7

#define Stepper3Dir 8
#define Stepper3Step 9
#define Stepper3En 13

#define Stepper4Dir 10
#define Stepper4Step 11
#define Stepper4En 12

#define Stepper5Dir A5
#define Stepper5Step A3
#define Stepper5En A4

#define STEPS 200 // steps per revolution
Stepper Stepper1(STEPS, Stepper1Dir, Stepper1Step);
Stepper Stepper2(STEPS, Stepper2Dir, Stepper2Step);
Stepper Stepper3(STEPS, Stepper3Dir, Stepper3Step);
Stepper Stepper4(STEPS, Stepper4Dir, Stepper4Step);
Stepper Stepper5(STEPS, Stepper5Dir, Stepper5Step);

int Speed = 600; // 1000 overturns, 700 overshoots bit (works but meh), 600 okay, 500 is good but tban bl'allergie
const int steppers_count = 5;
int SteppersEns[] = {Stepper1En, Stepper2En, Stepper3En, Stepper4En, Stepper5En};
Stepper Steppers[] = {Stepper1, Stepper2, Stepper3, Stepper4, Stepper5};

// serial communication variables
const int arrSize = 10;
String* parts_of_msg = new String[arrSize]; // according to the largest string array we'll need (ex. ANGLES 90 90 90 90 90)

// TEMP: the long variable must be pre-inited before using msg.toInt() in serial otherwise it'll cap out at 32k
long serialLongValue;


void setup() {
  
  // initialize relay pin
  pinMode(powerSupplyRelayPin, OUTPUT);

  // INIT: Serial
  Serial.begin(9600);
  while(!Serial){}

  // INIT: Stepper
  for(int i=0; i<steppers_count; i++){
    Steppers[i].setSpeed(Speed);
    pinMode(SteppersEns[i], OUTPUT);
    digitalWrite(SteppersEns[i], LOW); // disable pin
  }
  Serial.println("Ok, BTW You're overriding speed for B motor");
  Steppers[3].setSpeed(400);
  Steppers[4].setSpeed(400);
  

  // LOAD: Stepper location value from eeprom from last execution
  // FIRST LAUNCH CHECK: check if this is the first time this arduino was used for this code, if so pre-save default values
  float first_time = 0.0;
  EEPROM.get( 0, first_time );

  // 
  if (isnan(first_time) || first_time!=6.9) {
    EEPROM.put( 0, 6.9 ); // proves db was inited
    Serial.println("Ok, First time install executed");
  } else {
    Serial.println("Ok, Ready");
  }

  // turn on relay pin
  digitalWrite(powerSupplyRelayPin, HIGH);
}

void loop() {
  serial();
}


long defaultSteps = 200;
int i=0;

void serial(){
  
  // SERIAL: receive commands from serial
  if(Serial.available()){
    String msg = Serial.readStringUntil('\n');

    // split string by spaces
    getValues(msg);

    if(parts_of_msg[0] == "SEQUENCE"){ // SEQUENCE <Faces>    ex. SEQUENCE RUru   (sequence of turns, upper case=clockwise, lower case=anti-clockwise)
      // loop over each move of this sequence and execute it
      i = 0;
      while(i < parts_of_msg[1].length()){
        if(i < parts_of_msg[1].length() - 1){
          if(parts_of_msg[1][i+1] == '\''){
            turn(parts_of_msg[1][i], -defaultSteps);
            i++;
          } else if(parts_of_msg[1][i+1] == '2') {
            turn(parts_of_msg[1][i], defaultSteps*2);
            i++;
          } else
            turn(parts_of_msg[1][i], defaultSteps);
        } else {
          turn(parts_of_msg[1][i], defaultSteps);
        }
        //delay(100);
        i += 1;
      }
      Serial.println("Ok, finished the sequence " + String(parts_of_msg[1]));
      return;
    }

    if(parts_of_msg[0] == "MMOVE"){ // MMOVE <Face>    ex. MMOVE F2   or F'    or F
        if(parts_of_msg[1].length() > 1){
          if(parts_of_msg[1][1] == '\'')
            turn(parts_of_msg[1][0], -defaultSteps);
          else if(parts_of_msg[1][1] == '2')
            turn(parts_of_msg[1][0], defaultSteps*2);
          else
            turn(parts_of_msg[1][0], defaultSteps);
        } else {
          turn(parts_of_msg[1][0], defaultSteps);
        }
      Serial.println("Ok, finished the manual move " + String(parts_of_msg[1]));
      return;
    }

    if(parts_of_msg[0] == "MTURN"){ // MTURN <Face name> <amount>    ex. TURN  F2   or F'    or F 200  (manual turn)
      serialLongValue = parts_of_msg[2].toInt();
      
      if(parts_of_msg[1].length() > 1){
        if(parts_of_msg[1][1] == '\'')
          turn(parts_of_msg[1][0], -serialLongValue);
        else if(parts_of_msg[1][1] == '2')
          turn(parts_of_msg[1][0], serialLongValue*2);
        else
          turn(parts_of_msg[1][0], serialLongValue);
      } else {
        turn(parts_of_msg[1][0], serialLongValue);
      }
      Serial.println("Ok, finished manual turn of the " + String(parts_of_msg[1]) + " face by " + String(serialLongValue) + " steps");
      return;
    }
    
    Serial.println("OOF, Unknown command " + String(msg));
    return;
  }
}

void turn(char letter, long steps){
  if(letter == 'F'){
    moveStepper(0, -steps);
  } else if(letter == 'L'){
    moveStepper(1, steps);
  } else if(letter == 'R'){
    moveStepper(2, -steps);
  } else if(letter == 'D'){
    steps /= 2;
    if(abs(steps)==defaultSteps){
      moveStepper(3, steps<0 ? steps+3 : steps-3);
    } else {
      moveStepper(3, steps<0 ? steps+6 : steps-6);
    }
  } else if(letter == 'B'){
    steps /= 2;
    if(abs(steps)==defaultSteps){
      moveStepper(4, steps<0 ? -(steps+5) : -(steps-5));
    } else {
      moveStepper(4, steps<0 ? -(steps+10) : -(steps-10));
    }
  } else {
    Serial.println("OOF, Unknown turn name " + String(letter));
  }
}

void moveStepper(int index, long amount){
  //Serial.println("Ok, Moving stepper " + String(index+1) + " by " + String(amount) + " steps");
  digitalWrite(SteppersEns[index], HIGH);
  Steppers[index].step(amount);
  digitalWrite(SteppersEns[index], LOW);
}

unsigned int j = 0;
void getValues(String msg){
    j = 0;
    parts_of_msg[0] = "";
    for (unsigned int i = 0; i < msg.length(); i++) {
        if(j>=arrSize)
          break;
        if(msg[i]==' '){ j += 1; parts_of_msg[j] = ""; }
        else parts_of_msg[j] += msg[i];
    }
}
