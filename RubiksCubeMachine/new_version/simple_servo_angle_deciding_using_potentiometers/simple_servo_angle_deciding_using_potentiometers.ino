
/*
   this code contains two modes
   DEBUGGING MODE:
     (triggered by changing debugging variable to true)
     Allows you to use two potentiometers to move the servos around to decide angles of each
     of the Sleeve and wrist, values are printed in Serial

   NON-DEBUGGING MODE:
     (triggered by changing debugging varaible to false)
     Allows you to either write predefined moves or receiving cube turns from console and applying
     them

   NOTES:
     This code controls ten servo motors
*/


/*
  SELECT <L,R,U,D,B>
  DEBUG <1,0>
  MOTORS <RESET,ON,OFF>
  MOVE <LlRrUuDdBb> # MOVE is followed by a string of letters signifying the faces, upper case signifies clockwise turn, lower case signifies anti-clockwise
  ANGLE <WVER,WHOR,SBACK,SFRONT> <VALUE>
  ANGLE <W,S> <VALUE>
*/

// IMPORTS
#include <Servo.h>


// DEFINITIONS: General variables
int mode = 0;
bool enabled = true;
bool start = false;


// DEFINITIONS: DEBUGGING
// variables
bool debugging = false;
// Potentiometers
int next_poten1, next_poten2, next_poten3;
int previous_poten1 = 0, previous_poten2 = 0, previous_poten3 = 0;
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
Servo left_sleeve, left_wrist, up_sleeve, up_wrist, down_sleeve, down_wrist, back_sleeve, back_wrist, right_sleeve, right_wrist;

// DEFINTIONS: Predefined angles
// LEFT MECHANISM
int left_cw_start = 5, left_cw_end = 124, left_acw_start = 106, left_acw_end = 0;
int left_sleeve_back = 165, left_sleeve_forth = 0;
int left_sleeve_val = left_sleeve_back, left_wrist_val = left_cw_start;

// up MECHANISM
int up_cw_start = 55, up_cw_end = 174, up_acw_start = 158, up_acw_end = 45;
int up_sleeve_back = 180, up_sleeve_forth = 0;
int up_sleeve_val = up_sleeve_back, up_wrist_val = up_cw_start;

// down MECHANISM
int down_cw_start = 180, down_cw_end = 87, down_acw_start = 0, down_acw_end = 110;
int down_sleeve_back = 180, down_sleeve_forth = 63;
int down_sleeve_val = down_sleeve_back, down_wrist_val = down_cw_start;

// BACK MECHANISM
int up_assist_angle = 158, up_sleeve_assist_angle = 1;
int back_cw_start = 20, back_cw_end = 138, back_acw_start = 127, back_acw_end = 5;
int back_sleeve_back = 180, back_sleeve_forth = 0;
int back_sleeve_val = back_sleeve_back, back_wrist_val = back_cw_start;

// RIGHT MECHANISM
int right_cw_start = 9, right_cw_end = 129, right_acw_start = 108, right_acw_end = 0;
int right_sleeve_back = 165, right_sleeve_forth = 0;
int right_sleeve_val = right_sleeve_back, right_wrist_val = right_cw_start;

int moves_index = 0;
String moves_to_make = "";
bool Move = false;
int tempdelay = 50;

void setup() {

  // Step 1: Serial
  Serial.begin(9600);

  // Step 2: Attach servos
  attach_motors();
  resetMotorPositions();

  Serial.print("READY");
}

void loop() {
  receiveCommand();

  if (!start)
    return;

  if (debugging) {
    controlUsingPotentiometers();
  } else {
    if (Move)
      performReceivedMoves();
  }
}

void receiveCommand() {

  // Don't read from serial until you perform all of the moves you've received
  if (Move)
    return;

  if (Serial.available() > 0) {
    String request = Serial.readStringUntil('\n');
    String command = getValue(request, ' ', 0);

    if (command == "START") {
      start = true;
      Serial.println("Ok");
      return;
    }

    if (!start)
      return;

    // only allow selecting faces if we're in debug
    //if (debugging) {
      if (command == "SELECT") {
        selectFace(request);
        Serial.println("Ok");
        return;
      }
    //}

    if (command == "DEBUG") {
      String state = getValue(request, ' ', 1);
      debugging = state == "1";
      Serial.println("Ok");
      return;
    } else if (command == "MOTORS") {
      String order = getValue(request, ' ', 1);
      if (order == "RESET") {
        resetMotorPositions();
        Serial.println("Ok");
        return;
      } else if (order == "ON") {
        enabled = true;
        Serial.println("Ok");
        return;
      } else if (order == "OFF") {
        enabled = false;
        Serial.println("Ok");
        return;
      }
    } else if (command == "MOVE") {
      moves_to_make = getValue(request, ' ', 1);
      moves_index = 0;
      Move = true;
      return;
    } else if (command == "ANGLE") {
      String face = getValue(request, ' ', 1);
      if (face != "") {
        String rest_of_command = getValue(request, ' ', 2) + " " + getValue(request, ' ', 3);
        setAngle(face, rest_of_command);
        Serial.println("Ok");
        return;
      }
    }
    Serial.println("No");
  }
}

void preprocessManualAngleSet(String value, Servo &sleeve, Servo &wrist, int &min_s, int &max_s, int &min_w, int &max_w, int &typical_s, int &typical_w) {
  if (value == "WVER") {
    applyPotentiometerToFace(sleeve, wrist, typical_s, min_w);
  } else if (value == "WHOR") {
    applyPotentiometerToFace(sleeve, wrist, typical_s, max_w);
  } if (value == "SBACK") {
    applyPotentiometerToFace(sleeve, wrist, min_s, typical_w);
  } else if (value == "SFORTH") {
    applyPotentiometerToFace(sleeve, wrist, max_s, typical_w);
  } else {
    int val = getValue(value, ' ', 1).toInt();
    Serial.println(val);
    Serial.println(up_sleeve_back);
    Serial.println("yes");
    Serial.println(up_sleeve_val);
    Serial.println(typical_s);
    if (getValue(value, ' ', 0) == "W") {
      //applyPotentiometerToFace(sleeve, wrist, typical_s, val);
      go(wrist, typical_w, val, MEDIUM_SPEED);
    } else {
      //applyPotentiometerToFace(sleeve, wrist, val, typical_w);
      go(sleeve, typical_s, val, MEDIUM_SPEED);
    }
  }
}

void setAngle(String face, String value) {
  // Step 4: remap them and send them to our servos
  switch (face[0]) {
    case 'L':
      preprocessManualAngleSet(value, left_sleeve, left_wrist, left_cw_start, left_acw_start, left_sleeve_back, left_sleeve_forth, left_sleeve_val, left_wrist_val);
      break;
    case 'R':
      preprocessManualAngleSet(value, right_sleeve, right_wrist, right_cw_start, right_acw_start, right_sleeve_back, right_sleeve_forth, right_sleeve_val, right_wrist_val);
      break;
    case 'U':
      preprocessManualAngleSet(value, up_sleeve, up_wrist, up_cw_start, up_acw_start, up_sleeve_back, up_sleeve_forth, up_sleeve_val, up_wrist_val);
      break;
    case 'D':
      preprocessManualAngleSet(value, down_sleeve, down_wrist, down_cw_start, down_acw_start, down_sleeve_back, down_sleeve_forth, down_sleeve_val, down_wrist_val);
      break;
    case 'B':
      preprocessManualAngleSet(value, back_sleeve, back_wrist, back_cw_start, back_acw_start, back_sleeve_back, back_sleeve_forth, back_sleeve_val, back_wrist_val);
      break;
  }
}

void controlUsingPotentiometers() {
  // Step 1: read potentiometer values
  next_poten1 = analogRead(potentiometer1); next_poten2 = analogRead(potentiometer2); next_poten3 = analogRead(potentiometer3);

  // Step 2: check if there was an update from potentiometers
  if (previous_poten1 != next_poten1 ||  previous_poten2 != next_poten2 || previous_poten3 != next_poten3) {

    // Step 3: if so update our potentiometer values
    previous_poten1 = next_poten1; previous_poten2 = next_poten2; previous_poten3 = next_poten3;

    // Step 4: remap them and send them to our servos
    switch (mode) {
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
}

void performReceivedMoves() {

  if (moves_to_make == "")
    return;

  char c = moves_to_make[moves_index];
  switch (c) {
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
      Serial.println("No");
      moves_to_make = "";
      break;
  }

  // increment index
  moves_index += 1;
  // if we reachd the end of the string loop back to the starat
  if (moves_index >= moves_to_make.length() || moves_to_make == "") {
    moves_to_make = "";
    Move = false;
    moves_index = 0;

    Serial.println("Ok");
  }
}

void resetMotorPositions() {
  // Step 3: Retract servos
  // LEFT
  left_sleeve.write(left_sleeve_back);
  left_sleeve_val = left_sleeve_back;
  left_wrist.write(left_cw_start);
  left_wrist_val = left_cw_start;

  // up
  up_sleeve.write(up_sleeve_back);
  up_sleeve_val = up_sleeve_back;
  up_wrist.write(up_cw_start);
  up_wrist_val = up_cw_start;

  // down
  down_sleeve.write(down_sleeve_back);
  down_sleeve_val = down_sleeve_back;
  down_wrist.write(down_cw_start);
  down_wrist_val = down_cw_start;

  // BACK
  back_sleeve.write(back_sleeve_back);
  back_sleeve_val = back_sleeve_back;
  back_wrist.write(back_cw_start);
  back_wrist_val = back_cw_start;

  // RIGHT
  right_sleeve.write(right_sleeve_back);
  right_sleeve_val = right_sleeve_back;
  right_wrist.write(right_cw_start);
  right_wrist_val = right_cw_start;
}

void R(bool clockwise) {
  if (clockwise) {
    turn(right_wrist, right_sleeve, right_wrist_val, right_sleeve_val, right_cw_start, right_cw_end, right_sleeve_back, right_sleeve_forth, MEDIUM_SPEED);
  } else {
    turn(right_wrist, right_sleeve, right_wrist_val, right_sleeve_val, right_acw_start, right_acw_end, right_sleeve_back, right_sleeve_forth, MEDIUM_SPEED);
  }
}
void B(bool clockwise) {

  // bring up wrist in to pin middle layer in place
  go(up_wrist, up_wrist_val, up_assist_angle, MEDIUM_SPEED);
  go(up_sleeve, up_sleeve_val, up_sleeve_assist_angle, MEDIUM_SPEED);
  delay(tempdelay);

  if (clockwise) {
    turn(back_wrist, back_sleeve, back_wrist_val, back_sleeve_val, back_cw_start, back_cw_end, back_sleeve_back, back_sleeve_forth, MEDIUM_SPEED);
  } else {
    turn(back_wrist, back_sleeve, back_wrist_val, back_sleeve_val, back_acw_start, back_acw_end, back_sleeve_back, back_sleeve_forth, MEDIUM_SPEED);
  }

  // pull up wrist back up
  go(up_sleeve, up_sleeve_val, up_sleeve_back, MEDIUM_SPEED);
}
void L(bool clockwise) {
  if (clockwise) {
    turn(left_wrist, left_sleeve, left_wrist_val, left_sleeve_val, left_cw_start, left_cw_end, left_sleeve_back, left_sleeve_forth, MEDIUM_SPEED);
  } else {
    turn(left_wrist, left_sleeve, left_wrist_val, left_sleeve_val, left_acw_start, left_acw_end, left_sleeve_back, left_sleeve_forth, MEDIUM_SPEED);
  }
}
void D(bool clockwise) {
  if (clockwise) {
    turn(down_wrist, down_sleeve, down_wrist_val, down_sleeve_val, down_cw_start, down_cw_end, down_sleeve_back, down_sleeve_forth, MEDIUM_SPEED);
  } else {
    turn(down_wrist, down_sleeve, down_wrist_val, down_sleeve_val, down_acw_start, down_acw_end, down_sleeve_back, down_sleeve_forth, MEDIUM_SPEED);
  }
}
void U(bool clockwise) {
  if (clockwise) {
    turn(up_wrist, up_sleeve, up_wrist_val, up_sleeve_val, up_cw_start, up_cw_end, up_sleeve_back, up_sleeve_forth, MEDIUM_SPEED);
  } else {
    turn(up_wrist, up_sleeve, up_wrist_val, up_sleeve_val, up_acw_start, up_acw_end, up_sleeve_back, up_sleeve_forth, MEDIUM_SPEED);
  }
}

void selectFace(String command) {
  String face = getValue(command, ' ', 1);
  if (face == "") {
    Serial.println("No");
    return;
  }

  switch (face[0]) {
    case 'L':
      mode = 0;
      break;
    case 'R':
      mode = 1;
      break;
    case 'U':
      mode = 2;
      break;
    case 'D':
      mode = 3;
      break;
    case 'B':
      mode = 4;
      break;
    default:
      Serial.println("No");
      return;
      break;
  }
  Serial.println("Ok");
}

void applyPotentiometerToFace(Servo &sleeve, Servo &wrist, int &sleeve_val, int &wrist_val) {
  sleeve_val = map(previous_poten1, 0, 1023, 0, 180);
  wrist_val = map(previous_poten2, 0, 1023, 0, 180);
  sleeve.write(sleeve_val);
  wrist.write(wrist_val);

  // Servo 5: display potentiometer values
  Serial.println("Sleeve: " + String(sleeve_val, DEC) +
                 " Wrist: " + String(wrist_val, DEC));
}

void attach_motors() {
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
}

void turn(Servo &wrist, Servo &sleeve, int &wrist_val, int &sleeve_val, int Start, int End, int back, int forth, int Speed) {
  go(wrist, wrist_val, Start, Speed);
  go(sleeve, sleeve_val, forth, Speed);
  delay(tempdelay);
  go(wrist, wrist_val, End, Speed);
  delay(tempdelay);
  go(sleeve, sleeve_val, back, Speed);
}

void go(Servo &servo, int &departing_angle, int destination_angle, int Speed) {

  if(departing_angle==destination_angle)
    return;

  if (destination_angle > 180)
    destination_angle = 180;
  else if (destination_angle < 0)
    destination_angle = 0;

  int Direction = destination_angle > departing_angle ? 1 : -1;
  int difference = abs(destination_angle - departing_angle);
  for (int i = 0; i < difference; i++) {
    departing_angle += Direction;
    servo.write(departing_angle);
    delay(Speed);
  }

  departing_angle = destination_angle;
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
