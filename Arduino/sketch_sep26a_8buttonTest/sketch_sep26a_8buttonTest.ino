#include <Servo.h>

const int servoPinA = 2;
const int servoPinB = 3;

Servo servoA;
Servo servoB;

const int dataPin = 11;
const int clockPin = 12;
const int loadPin = 8;
const int clockEnablePin = 9;

byte incoming;

void setup() {
  
  //servoA.attach(servoPinA);
  //servoB.attach(servoPinB);

  pinMode(dataPin,OUTPUT);
  pinMode(clockPin,OUTPUT);
  pinMode(loadPin,OUTPUT);
  pinMode(clockEnablePin,OUTPUT);

  digitalWrite(clockPin, HIGH);
  digitalWrite(loadPin, HIGH);
  
  Serial.begin(9600);
}

void loop() {
  incoming = read_shift_regs();

  Serial.println("\nThe incoming values of the shift register : ");
  Serial.print("ABCDEFGH : ");

  byte hmm = incoming;
  print_byte(incoming);
  
  //if(!(hmm - 2 ==1)){ servoA.write(0);}
  //else{ servoA.write(90); }
  
  delay(2000);
}

byte read_shift_regs()
{
  byte the_shifted = 0;  // An 8 bit number to carry each bit value of A-H

  // Trigger loading the state of the A-H data lines into the shift register
  digitalWrite(loadPin, LOW);
  delayMicroseconds(5); // Requires a delay here according to the datasheet timing diagram
  digitalWrite(loadPin, HIGH);
  delayMicroseconds(5);

  // Required initial states of these two pins according to the datasheet timing diagram
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, INPUT);
  digitalWrite(clockPin, HIGH);
  digitalWrite(clockEnablePin, LOW); // Enable the clock

  // Get the A-H values
  the_shifted = shiftIn(dataPin, clockPin, MSBFIRST);
  digitalWrite(clockEnablePin, HIGH); // Disable the clock
  return the_shifted;
}
void print_byte(byte val)
{
    byte i;
    for(byte i=0; i<=7; i++)
    {
      Serial.print(val >> i & 1, BIN); // Magic bit shift, if you care look up the <<, >>, and & operators
    }
    Serial.print("\n"); // Go to the next line, do not collect $200
}
