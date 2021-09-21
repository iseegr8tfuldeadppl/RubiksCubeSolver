#include <Servo.h>
Servo Servo1;
Servo Servo2;
Servo Servo3;
Servo Servo4;
Servo Servo5;


int servo1_one_turn = 1000;
int servo2_one_turn = 1000;
int servo3_one_turn = 1000;
int servo4_one_turn = 1000;
int servo5_one_turn = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW);
  //Servo1.attach(2);
  //Servo2.attach(4);
  //Servo3.attach(7);
  //Servo4.attach(9);
  //Servo5.attach(10);
}

void loop() {
  if(Serial.available() > 0) {
    Serial.println("Looping");
        
    // Step 1: read the incoming message:
    char received = Serial.read();

    switch(received){
      case '1':
        Serial.println("Turning Servo 1 clockwise");
        digitalWrite(3, HIGH);
        Servo1.attach(2); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo1.write(180); //clockwise rotation 
        delay(servo1_one_turn); //rotation duration in ms 
        Servo1.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case 'a':
        Serial.println("Turning Servo 1 anticlockwise");
        digitalWrite(3, HIGH);
        Servo1.attach(2); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo1.write(0); //clockwise rotation 
        delay(servo1_one_turn); //rotation duration in ms 
        Servo1.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case '2':
        Serial.println("Turning Servo 2 clockwise");
        digitalWrite(3, HIGH);
        Servo2.attach(4); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo2.write(180); //clockwise rotation 
        delay(servo2_one_turn); //rotation duration in ms 
        Servo2.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case 'b':
        Serial.println("Turning Servo 2 anticlockwise");
        digitalWrite(3, HIGH);
        Servo2.attach(4); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo2.write(0); //clockwise rotation 
        delay(servo2_one_turn); //rotation duration in ms 
        Servo2.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case '3':
        Serial.println("Turning Servo 3 clockwise");
        digitalWrite(3, HIGH);
        Servo3.attach(7); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo3.write(180); //clockwise rotation 
        delay(servo3_one_turn); //rotation duration in ms 
        Servo3.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case 'c':
        Serial.println("Turning Servo 3 anticlockwise");
        digitalWrite(3, HIGH);
        Servo3.attach(7); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo3.write(0); //clockwise rotation 
        delay(servo3_one_turn); //rotation duration in ms 
        Servo3.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case '4':
        Serial.println("Turning Servo 4 clockwise");
        Servo4.attach(9); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo4.write(180); //clockwise rotation 
        delay(servo4_one_turn); //rotation duration in ms 
        Servo4.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case 'd':
        Serial.println("Turning Servo 4 anticlockwise");
        digitalWrite(3, HIGH);
        Servo4.attach(9); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo4.write(0); //clockwise rotation 
        delay(servo4_one_turn); //rotation duration in ms 
        Servo4.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case '5':
        Serial.println("Turning Servo 5 clockwise");
        digitalWrite(3, HIGH);
        Servo5.attach(10); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo5.write(180); //clockwise rotation 
        delay(servo5_one_turn); //rotation duration in ms 
        Servo5.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      case 'e':
        Serial.println("Turning Servo 5 anticlockwise");
        digitalWrite(3, HIGH);
        Servo5.attach(10); //reattach servo to pin 9 before looping 
        // infinite spin on pin 9
        Servo5.write(0); //clockwise rotation 
        delay(servo5_one_turn); //rotation duration in ms 
        Servo5.detach(); //detach servo to prevent “creeping” effect 
        digitalWrite(3, LOW);
        break;
      default:
        break;
    }
  }
      
}
