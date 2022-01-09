#include <Servo.h>
#include <EEPROM.h>

boolean reset = false;
String msg = "";

Servo bottom, front, left, back, right;
int bottom_pin=3, front_pin=5, left_pin=6, back_pin=9, right_pin=10;

boolean bottom_turning=false, front_turning=false, left_turning=false, back_turning=false, right_turning=false;
int bottom_speed = 50, front_speed = 50, left_speed = 50, back_speed = 50, right_speed = 50;

int bottom_turntime=220, front_turntime=195, left_turntime=220, back_turntime=220, right_turntime=220;
int bottom_rest_angle=95, front_rest_angle=90, left_rest_angle=10, back_rest_angle=0, right_rest_angle=127;

void setup() {
  Serial.begin(9600);
  
  bottom.attach(bottom_pin);
  front.attach(front_pin);
  left.attach(left_pin);
  back.attach(back_pin);
  right.attach(right_pin);

  if(reset){
    EEPROM.put( 0, bottom_rest_angle );
    EEPROM.put( 10, front_rest_angle );
    EEPROM.put( 20, left_rest_angle );
    EEPROM.put( 30, back_rest_angle );
    EEPROM.put( 40, right_rest_angle );
    
    EEPROM.put( 50, bottom_turntime );
    EEPROM.put( 60, front_turntime );
    EEPROM.put( 70, left_turntime );
    EEPROM.put( 80, back_turntime );
    EEPROM.put( 90, right_turntime );
    
    EEPROM.put( 100, bottom_speed );
    EEPROM.put( 120, front_speed );
    EEPROM.put( 130, left_speed );
    EEPROM.put( 140, back_speed );
    EEPROM.put( 150, right_speed );
  } else {
    EEPROM.get( 0, bottom_rest_angle );
    EEPROM.get( 10, front_rest_angle );
    EEPROM.get( 20, left_rest_angle );
    EEPROM.get( 30, back_rest_angle );
    EEPROM.get( 40, right_rest_angle );
    
    EEPROM.get( 50, bottom_turntime );
    EEPROM.get( 60, front_turntime );
    EEPROM.get( 70, left_turntime );
    EEPROM.get( 80, back_turntime );
    EEPROM.get( 90, right_turntime );
    
    EEPROM.get( 100, bottom_speed );
    EEPROM.get( 120, front_speed );
    EEPROM.get( 130, left_speed );
    EEPROM.get( 140, back_speed );
    EEPROM.get( 150, right_speed );
  }

  report();

  bottom.write(bottom_rest_angle);
  front.write(front_rest_angle);
  left.write(left_rest_angle);
  back.write(back_rest_angle);
  right.write(right_rest_angle);
}


void loop() {
  readSerial();
}


void readSerial(){
  if (Serial.available()) {
    char lil = Serial.read();
    if (lil == '\n') {
      treat_command();
      msg = "";
    } else {
      msg.concat(lil);
    }
  }
}


void treat_command(){
  Serial.println(msg);
  
  String command = getValue(msg, ' ', 0);
  if (command == "RESTANGLE") {
    update_rest_angle();
    
  } else if (command == "TURNTIME") { // TURNTIME F' 220
    update_turn_time();
  } else if (command == "TURN") { // TURN F'sssss
    turn();
  } else if (command == "TOGGLEMOTOR") { // TOGGLEMOTOR F'
    toggle();
  } else if (command == "SPEED") { // SPEED F 50
    update_speed();
  } else if (command == "REPORT") { // REPORT
    report();
  } else if (command == "TURNS") { // TURNS FDR'L'B'BF'LR
    turns();
  } else {
    Serial.println("No, unknown command " + command);
  }
}



void turns() {

  String moves_to_make = getValue(msg, ' ', 1);

  if (moves_to_make == "")
    return;

  int moves_index = 0;
  while(true){
    delay(300);
    char c = moves_to_make[moves_index];
    switch (c) {
      case 'D':
        D(true);
        break;
      case 'd':
        D(false);
        break;
        
      case 'F':
        F_(true);
        break;
      case 'f':
        F_(false);
        break;
        
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
        
      case 'B':
        B(true);
        break;
      case 'b':
        B(false);
        break;
        
      default:
        Serial.println("No, unrecognized character " + String(c));
        break;
    }
  
    // increment index
    moves_index += 1;
    // if we reachd the end of the string loop back to the starat
    if (moves_index >= moves_to_make.length()) {
      moves_to_make = "";
      Serial.println("Ok");
      return;
    }
  }
}


void report(){
  Serial.println("Rest Angles: D " + String(bottom_rest_angle, DEC)
                    + " F " + String(front_rest_angle)
                    + " L " + String(left_rest_angle)
                    + " B " + String(back_rest_angle)
                    + " R " + String(right_rest_angle));
  Serial.println("Turn Times: D " + String(bottom_turntime)
                    + " F " + String(front_turntime)
                    + " L " + String(left_turntime)
                    + " B " + String(back_turntime)
                    + " R " + String(right_turntime));
  Serial.println("Speeds: D " + String(bottom_speed)
                    + " F " + String(front_speed)
                    + " L " + String(left_speed)
                    + " B " + String(back_speed)
                    + " R " + String(right_speed));
}


void toggle(){
  String face = getValue(msg, ' ', 1);
  
  if(face=="D"){
    if(bottom_turning)
      bottom.write(bottom_rest_angle);
    else
      bottom.write(bottom_rest_angle+bottom_speed);
    bottom_turning = !bottom_turning;
    
  } else if(face=="F"){
    if(front_turning)
      front.write(front_rest_angle);
    else
      front.write(front_rest_angle+front_speed);
    front_turning = !front_turning;
  
  } else if(face=="L"){
    if(left_turning)
      left.write(left_rest_angle);
    else
      left.write(left_rest_angle+left_speed);
    left_turning = !left_turning;
    
  } else if(face=="B"){
    if(back_turning)
      back.write(back_rest_angle);
    else
      back.write(back_rest_angle+back_speed);
    back_turning = !back_turning;
    
  } else if(face=="R"){
    if(right_turning)
      right.write(right_rest_angle);
    else
      right.write(right_rest_angle+right_speed);
    right_turning = !right_turning;

    
  } else if(face=="D'"){
    if(bottom_turning)
      bottom.write(bottom_rest_angle);
    else
      bottom.write(bottom_rest_angle-bottom_speed);
    bottom_turning = !bottom_turning;
    
  } else if(face=="F'"){
    if(front_turning)
      front.write(front_rest_angle);
    else
      front.write(front_rest_angle-front_speed);
    front_turning = !front_turning;
  
  } else if(face=="L'"){
    if(left_turning)
      left.write(left_rest_angle);
    else
      left.write(left_rest_angle-front_speed);
    left_turning = !left_turning;
    
  } else if(face=="B'"){
    if(back_turning)
      back.write(back_rest_angle);
    else
      back.write(back_rest_angle-back_speed);
    back_turning = !back_turning;
    
  } else if(face=="R'"){
    if(right_turning)
      right.write(right_rest_angle);
    else
      right.write(right_rest_angle-right_speed);
    right_turning = !right_turning;
    
  } else {
    Serial.println("No, unrecognized face " + face);
  }
}

void D(boolean cw_acw){
  if(cw_acw){
    bottom.write(bottom_rest_angle+bottom_speed);
    delay(bottom_turntime);
    bottom.write(bottom_rest_angle);
  } else {
    bottom.write(bottom_rest_angle-bottom_speed);
    delay(bottom_turntime);
    bottom.write(bottom_rest_angle);
  }
}

void F_(boolean cw_acw){
  if(cw_acw){
    front.write(front_rest_angle+front_speed);
    delay(front_turntime);
    front.write(front_rest_angle);
  } else {
    front.write(front_rest_angle-front_speed);
    delay(front_turntime);
    front.write(front_rest_angle);
  }
}

void L(boolean cw_acw){
  if(cw_acw){
    left.write(left_rest_angle+left_speed);
    delay(left_turntime);
    left.write(left_rest_angle);
  } else {
    left.write(left_rest_angle-left_speed);
    delay(left_turntime);
    left.write(left_rest_angle);
  }
}

void B(boolean cw_acw){
  if(cw_acw){
    back.write(back_rest_angle+back_speed);
    delay(back_turntime);
    back.write(back_rest_angle);
  } else {
    back.write(back_rest_angle-back_speed);
    delay(back_turntime);
    back.write(back_rest_angle);
  }
}

void R(boolean cw_acw){
  if(cw_acw){
    right.write(right_rest_angle+right_speed);
    delay(right_turntime);
    right.write(right_rest_angle);
  } else {
    right.write(right_rest_angle-right_speed);
    delay(right_turntime);
    right.write(right_rest_angle);
  }
}

void turn(){
  String face = getValue(msg, ' ', 1);

  if(face=="D"){
    D(true);
  } else if(face=="F"){
    F_(true);
  } else if(face=="L"){
    L(true);
  } else if(face=="B"){
    B(true);
  } else if(face=="R"){
    R(true);
  } else if(face=="D'"){
    D(false);
    
  } else if(face=="F'"){
    F_(false);
  } else if(face=="L'"){
    L(false);
  } else if(face=="B'"){
    B(false);
  } else if(face=="R'"){
    R(false);
    
  } else {
    Serial.println("No, unrecognized face " + face);
  }
}


void update_turn_time(){
  String face = getValue(msg, ' ', 1);

  String TimeStr = getValue(msg, ' ', 2);
  int Time = TimeStr.toInt();

  if(isnan(Time)){
    Serial.println("No, invalid turn time " + TimeStr);
  } else {

    // TODO: cap turn time between 0 and inf
    if(Time<0) Time = 0;
    
    if(face=="D"){
      bottom_turntime = Time;
      EEPROM.put( 50, bottom_turntime );
      
    } else if(face=="F"){
      front_turntime = Time;
      EEPROM.put( 60, front_turntime );
    
    } else if(face=="L"){
      left_turntime = Time;
      EEPROM.put( 70, left_turntime );
      
    } else if(face=="B"){
      back_turntime = Time;
      EEPROM.put( 80, back_turntime );
      
    } else if(face=="R"){
      right_turntime = Time;
      EEPROM.put( 90, right_turntime );
      
    } else {
      Serial.println("No, unrecognized face " + face);
    }
  }
}



void update_speed(){
  String face = getValue(msg, ' ', 1);

  String SpeedStr = getValue(msg, ' ', 2);
  int Speed = SpeedStr.toInt();

  if(isnan(Speed)){
    Serial.println("No, invalid speed " + SpeedStr);
  } else {
    
    if(face=="D"){
      bottom_speed = Speed;
      EEPROM.put( 100, bottom_speed );
      
    } else if(face=="F"){
      front_speed = Speed;
      EEPROM.put( 110, front_speed );
    
    } else if(face=="L"){
      left_speed = Speed;
      EEPROM.put( 120, left_speed );
      
    } else if(face=="B"){
      back_speed = Speed;
      EEPROM.put( 130, back_speed );
      
    } else if(face=="R"){
      right_speed = Speed;
      EEPROM.put( 140, right_speed );
      
    } else {
      Serial.println("No, unrecognized face " + face);
    }
  }
}


void update_rest_angle(){
  String face = getValue(msg, ' ', 1);

  String angleStr = getValue(msg, ' ', 2);
  int angle = angleStr.toInt();

  if(isnan(angle)){
    Serial.println("No, invalid angle " + angleStr);
  } else {

    // TODO: cap angle between 0 and 180
    
    if(face=="D"){
      bottom_rest_angle = angle;
      EEPROM.put( 0, bottom_rest_angle );
      bottom.write(bottom_rest_angle);
      
    } else if(face=="F"){
      front_rest_angle = angle;
      EEPROM.put( 10, front_rest_angle );
      front.write(front_rest_angle);
    
    } else if(face=="L"){
      left_rest_angle = angle;
      EEPROM.put( 20, left_rest_angle );
      left.write(left_rest_angle);
      
    } else if(face=="B"){
      back_rest_angle = angle;
      EEPROM.put( 30, back_rest_angle );
      back.write(back_rest_angle);
      
    } else if(face=="R"){
      right_rest_angle = angle;
      EEPROM.put( 40, right_rest_angle );
      right.write(right_rest_angle);
      
    } else {
      Serial.println("No, unrecognized face " + face);
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
