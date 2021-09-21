
/*
 * this code contains two modes
 * DEBUGGING MODE:
 *   (triggered by changing debugging variable to true)
 *   Allows you to use two potentiometers to move the servos around to decide angles of each
 *   of the Sleeve and wrist, values are printed in Serial
 *   
 * NON-DEBUGGING MODE:
 *   (triggered by changing debugging varaible to false)
 *   Allows you to either write predefined moves or receiving cube turns from console and applying
 *   them
 * 
 * NOTES:
 *   This code controls ten servo motors
 */

// IMPORTS
#include <Servo.h>


// DEFINITIONS: General variables
int mode = 0;
bool enabled = false;


// DEFINITIONS: DEBUGGING
// variables
bool debugging = true;
// Potentiometers
int next_poten1, next_poten2, next_poten3;
int previous_poten1=0, previous_poten2=0, previous_poten3=0;
#define potentiometer1 A0
#define potentiometer2 A1
#define potentiometer3 A6


// DEFINITIONS: Speeds
int SLOW_SPEED = 5, MEDIUM_SPEED = 2, FASTAFBOI_SPEED = 1;


// DEFINITIONS: Servo Pins
#define left_sleeve_pin 9
#define left_wrist_pin 6
#define up_wrist_pin 5
#define up_sleeve_pin 3
#define down_wrist_pin 11
#define down_sleeve_pin 10
#define back_wrist_pin A2
#define back_sleeve_pin A3
#define right_wrist_pin A4
#define right_sleeve_pin A5

// DEFINITIONS: Servos Themselves
Servo left_sleeve,left_wrist, up_sleeve,up_wrist, down_sleeve,down_wrist, back_sleeve,back_wrist, right_sleeve,right_wrist;

// DEFINTIONS: Predefined angles
// LEFT MECHANISM
int left_cw_start = 5, left_cw_end = 124, left_acw_start = 106, left_acw_end = 0;
int left_sleeve_back = 163, left_sleeve_forth = 46;
int left_sleeve_val = left_sleeve_back, left_wrist_val = left_cw_start;

// up MECHANISM
int up_cw_start = 55, up_cw_end = 174, up_acw_start = 158, up_acw_end = 45;
int up_sleeve_back = 180, up_sleeve_forth = 0;
int up_sleeve_val = up_sleeve_back, up_wrist_val = up_cw_start;

// down MECHANISM
int down_cw_start = 180, down_cw_end = 67, down_acw_start = 0, down_acw_end = 118;
int down_sleeve_back = 180, down_sleeve_forth = 41;
int down_sleeve_val = down_sleeve_back, down_wrist_val = down_cw_start;
    
// BACK MECHANISM
int up_assist_angle = 158, up_sleeve_assist_angle = 1;
int back_cw_start = 20, back_cw_end = 138, back_acw_start = 127, back_acw_end = 5;
int back_sleeve_back = 151, back_sleeve_forth = 0;
int back_sleeve_val = back_sleeve_back, back_wrist_val = back_cw_start;

// RIGHT MECHANISM
int right_cw_start = 9, right_cw_end = 129, right_acw_start = 108, right_acw_end = 0;
int right_sleeve_back = 180, right_sleeve_forth = 0;
int right_sleeve_val = right_sleeve_back, right_wrist_val = right_cw_start;

char string[] = "RLDlUBRDrBu";
String messago = "";
int moves_index = 0;
String runMode="serial"; //Modes available: stringiteration          clockwiseanticlockwiselooptest
    
void setup() {

  // Step 1: Serial
  Serial.begin(9600);

  // Step 2: Attach servos
  left_sleeve.attach(left_sleeve_pin);
  left_wrist.attach(left_wrist_pin);
  up_sleeve.attach(up_sleeve_pin);
  up_wrist.attach(up_wrist_pin);
  down_sleeve.attach(down_sleeve_pin);
  down_wrist.attach(down_wrist_pin);
  back_sleeve.attach(back_sleeve_pin);
  back_wrist.attach(back_wrist_pin);
  right_sleeve.attach(right_sleeve_pin);
  right_wrist.attach(right_wrist_pin);

  resetMotorPositions();

  Serial.print("runMode=" + runMode);
}

void loop() {    
  if(debugging){
    readSerial();
    
    // Step 1: read potentiometer values
    next_poten1 = analogRead(potentiometer1); next_poten2 = analogRead(potentiometer2); next_poten3 = analogRead(potentiometer3);
  
    // Step 2: check if there was an update from potentiometers
    if(previous_poten1!=next_poten1 ||  previous_poten2!=next_poten2 || previous_poten3!=next_poten3){
      
      // Step 3: if so update our potentiometer values
      previous_poten1 = next_poten1; previous_poten2 = next_poten2; previous_poten3 = next_poten3;
  
      // Step 4: remap them and send them to our servos
      switch(mode){
        case 0:
        applyPotentiometerToFace(left_sleeve, left_wrist, left_sleeve_val, left_wrist_val);
          break;
        case 1:
          applyPotentiometerToFace(right_sleeve, right_wrist, right_sleeve_val, right_wrist_val);
          break;
        case 2:
          applyPotentiometerToFace(up_sleeve, up_wrist, up_sleeve_val, up_wrist_val);
          break;
        case 3:
          applyPotentiometerToFace(down_sleeve, down_wrist, down_sleeve_val, down_wrist_val);
          break;
        case 4:
          applyPotentiometerToFace(back_sleeve, back_wrist, back_sleeve_val, back_wrist_val);
          break;
      }

    }
  } else {
      if(runMode=="serial"){
        if(messago=="")
          readMovesFromSerial();
        else {
          char c = messago[moves_index];
          switch(c){
            case 'L':
              L(true);
              break;
            case 'l':
              L(false);
              break;
            case 'R':
              R(true);
              break;
            case 'r':
              R(false);
              break;
            case 'U':
              U(true);
              break;
            case 'u':
              U(false);
              break;
            case 'D':
              D(true);
              break;
            case 'd':
              D(false);
              break;
            case 'B':
              B(true);
              break;
            case 'b':
              B(false);
              break;
            default:
              Serial.println("Unknown move in string: " + String(c));
              Serial.println("Fail");
              break;
          }
          
          // increment index
          moves_index += 1;
          // if we reachd the end of the string loop back to the starat
          if(moves_index>=strlen(string)){
            messago = "";
            moves_index = 0;
            Serial.println("Ok");
          }
        }
    }     
    if(enabled){
      if(runMode=="stringiteration"){
        readSerial();

        // reset all motors before starting sequence
        if(moves_index==0)
          resetMotorPositions();
        
        char c = string[moves_index];
        switch(c){
          case 'L':
            L(true);
            break;
          case 'l':
            L(false);
            break;
          case 'R':
            R(true);
            break;
          case 'r':
            R(false);
            break;
          case 'U':
            U(true);
            break;
          case 'u':
            U(false);
            break;
          case 'D':
            D(true);
            break;
          case 'd':
            D(false);
            break;
          case 'B':
            B(true);
            break;
          case 'b':
            B(false);
            break;
          default:
            Serial.println("Unknown move in string: " + String(c));
            break;
        }
        
        // increment index
        moves_index += 1;
        // if we reachd the end of the string loop back to the starat
        if(moves_index>=strlen(string))
          moves_index = 0;
      } else if(runMode=="clockwiseanticlockwiselooptest"){
        readSerial();
        // predefined set of moves
        // these values are just clockwise/anti-clockwise loops to test each face
        switch(mode){
          case 0: // LEFT
            L(true); // clockwise
            delay(1500);
            L(false); // anti-clockwise
            delay(1500);
            break;
          case 1: // RIGHT
            R(true); // clockwise
            delay(1500);
            R(false); // anti-clockwise
            delay(1500);
            break;
          case 2: // UP
            U(true); // clockwise
            delay(1500);
            U(false); // anti-clockwise
            delay(1500);
            break;
          case 3: // DOWN
            D(true); // clockwise
            delay(1500);
            D(false); // anti-clockwise
            delay(1500);
            break;
          case 4: // BACK
            B(true); // clockwise
            delay(1500);
            B(false); // anti-clockwise
            delay(1500);
            break;
        } 
      }

    }

  }

}


void readMovesFromSerial(){
  if(Serial.available()>0){
    String message = Serial.readStringUntil('\n');
    if(message=='1'){
        Serial.println("DEBUG MODE: Exited debug mode");
        resetMotorPositions();
        debugging = false;
    } else if(message=='0'){
        Serial.println("DEBUG MODE: Entered debug mode");
        resetMotorPositions();
        debugging = true;
    } else if(message=='e'){
        Serial.println("Motors enabled");
        resetMotorPositions();
        enabled = true;
    } else if(message=='s'){
        Serial.println("Motors disabled");
        resetMotorPositions();
        enabled = false;
    } else if(message=='p'){
        Serial.println("runMode=stringiteration");
        runMode="stringiteration";
    } else if(message=='o'){
        Serial.println("runMode=clockwiseanticlockwiselooptest");
        runMode="clockwiseanticlockwiselooptest";
    } else {
      if(messago!=""){
        Serial.println("Fail");
      } else {
        messago = message;
      }
    }
  }
}

void readSerial(){
  while(Serial.available()>0){
    char letter = Serial.read();
    switch(letter){
      case 'L':
        Serial.println("DEBUG MODE: Selected face is L");
        mode = 0;
        break;
      case 'R':
        Serial.println("DEBUG MODE: Selected face is R");
        mode = 1;
        break;
      case 'U':
        Serial.println("DEBUG MODE: Selected face is U");
        mode = 2;
        break;
      case 'D':
        Serial.println("DEBUG MODE: Selected face is D");
        mode = 3;
        break;
      case 'B':
        Serial.println("DEBUG MODE: Selected face is B");
        mode = 4;
        break;
      case '1':
        Serial.println("DEBUG MODE: Exited debug mode");
        resetMotorPositions();
        debugging = false;
        break;
      case '0':
        Serial.println("DEBUG MODE: Entered debug mode");
        resetMotorPositions();
        debugging = true;
        break;
      case 'e':
        Serial.println("Motors enabled");
        resetMotorPositions();
        enabled = true;
        break;
      case 's':
        Serial.println("Motors disabled");
        resetMotorPositions();
        enabled = false;
        break;
      case 'm':
        resetMotorPositions();
        break;
      case 'p':
        Serial.println("runMode=stringiteration");
        runMode="stringiteration";
        moves_index = 0;
        break;
      case 'o':
        Serial.println("runMode=clockwiseanticlockwiselooptest");
        runMode="clockwiseanticlockwiselooptest";
        moves_index = 0;
        break;
      case 'g':
        Serial.println("runMode=serial");
        runMode="serial";
        moves_index = 0;
        break;
      case '\n':
        // just a new line indicator, comes at the end of every message
        break;
      default:
        Serial.println("Error: letter " + String(letter) + " is not recognized as a command");
        Serial.println("Type either L, R, U, D or B to choose a face");
        if(debugging){
          Serial.println("DEBUG MODE: After that you can control it with the two knobs");
        } else {
          Serial.println("Type e to enable motors or d to disable motors");
        }
        break;
    }
  }
}

void resetMotorPositions(){
  Serial.println("Resetted all motor positions");
  // Step 3: Retract servos
  // LEFT
  left_sleeve.write(left_sleeve_val);
  left_wrist.write(left_wrist_val);
  
  // up
  up_sleeve.write(up_sleeve_val);
  up_wrist.write(up_wrist_val);
  
  // down
  down_sleeve.write(down_sleeve_val);
  down_wrist.write(down_wrist_val);
  
  // BACK
  back_sleeve.write(back_sleeve_val);
  back_wrist.write(back_wrist_val);
  
  // RIGHT
  right_sleeve.write(right_sleeve_val);
  right_wrist.write(right_wrist_val);
}

void applyPotentiometerToFace(Servo &sleeve, Servo &wrist, int &sleeve_val, int &wrist_val){
    sleeve_val = map(previous_poten1, 0, 1023, 0, 180);
    wrist_val = map(previous_poten2, 0, 1023, 0, 180);
    sleeve.write(sleeve_val);
    wrist.write(wrist_val);

    // Servo 5: display potentiometer values
    Serial.println("Sleeve: " + String(sleeve_val, DEC) + 
                    " Wrist: " + String(wrist_val, DEC));
}

int tempdelay = 50;
void R(bool clockwise){
    if(clockwise){
      turn(right_wrist, right_sleeve, right_wrist_val, right_sleeve_val, right_cw_start, right_cw_end, right_sleeve_back, right_sleeve_forth, MEDIUM_SPEED);
    } else {
      turn(right_wrist, right_sleeve, right_wrist_val, right_sleeve_val, right_acw_start, right_acw_end, right_sleeve_back, right_sleeve_forth, MEDIUM_SPEED);
    }
}

void B(bool clockwise){
  
    // bring up wrist in to pin middle layer in place
    go(up_wrist, up_wrist_val, up_assist_angle, MEDIUM_SPEED);
    go(up_sleeve, up_sleeve_val, up_sleeve_assist_angle, MEDIUM_SPEED);
    delay(tempdelay);
    
    if(clockwise){
      turn(back_wrist, back_sleeve, back_wrist_val, back_sleeve_val, back_cw_start, back_cw_end, back_sleeve_back, back_sleeve_forth, MEDIUM_SPEED);
    } else {
      turn(back_wrist, back_sleeve, back_wrist_val, back_sleeve_val, back_acw_start, back_acw_end, back_sleeve_back, back_sleeve_forth, MEDIUM_SPEED);
    }
      
    // pull up wrist back up
    go(up_sleeve, up_sleeve_val, up_sleeve_back, MEDIUM_SPEED);
}

void L(bool clockwise){
    if(clockwise){
      turn(left_wrist, left_sleeve, left_wrist_val, left_sleeve_val, left_cw_start, left_cw_end, left_sleeve_back, left_sleeve_forth, MEDIUM_SPEED);
    } else {
      turn(left_wrist, left_sleeve, left_wrist_val, left_sleeve_val, left_acw_start, left_acw_end, left_sleeve_back, left_sleeve_forth, MEDIUM_SPEED);
    }
}

void D(bool clockwise){
    if(clockwise){
      turn(down_wrist, down_sleeve, down_wrist_val, down_sleeve_val, down_cw_start, down_cw_end, down_sleeve_back, down_sleeve_forth, MEDIUM_SPEED);
    } else {
      turn(down_wrist, down_sleeve, down_wrist_val, down_sleeve_val, down_acw_start, down_acw_end, down_sleeve_back, down_sleeve_forth, MEDIUM_SPEED);
    }
}
void U(bool clockwise){
    if(clockwise){
      turn(up_wrist, up_sleeve, up_wrist_val, up_sleeve_val, up_cw_start, up_cw_end, up_sleeve_back, up_sleeve_forth, MEDIUM_SPEED);
    } else {
      turn(up_wrist, up_sleeve, up_wrist_val, up_sleeve_val, up_acw_start, up_acw_end, up_sleeve_back, up_sleeve_forth, MEDIUM_SPEED);
    }
}

void turn(Servo &wrist, Servo &sleeve, int &wrist_val, int &sleeve_val, int Start, int End, int back, int forth, int Speed){
  go(wrist, wrist_val, Start, Speed);
  go(sleeve, sleeve_val, forth, Speed);
  delay(tempdelay);
  go(wrist, wrist_val, End, Speed);
  delay(tempdelay);
  go(sleeve, sleeve_val, back, Speed);
}

void go(Servo &servo, int &departing_angle, int destination_angle, int Speed){
  int Direction = destination_angle > departing_angle? 1 : -1;
  int difference = abs(destination_angle - departing_angle);
  for(int i=0; i<difference; i++){
    departing_angle += Direction;
    servo.write(departing_angle);
    delay(Speed);
  }

  departing_angle = destination_angle;
}
