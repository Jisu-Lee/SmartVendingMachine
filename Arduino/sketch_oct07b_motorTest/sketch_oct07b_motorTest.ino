
#include <Servo.h>

int servo2_pin = 2;
int btn_pin = 13;
int btn_state = 0;

Servo servo2, servo7, servo9;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  servo2.attach(servo2_pin);
  pinMode(btn_pin, INPUT);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  btn_state = digitalRead(btn_pin);

  Serial.print("btn = ");
  Serial.println(btn_state);
  
  if(btn_state == LOW){
    //servo9.write(0);
    servo2.write(0);
    //servo7.write(0);
    delay(1000);    
  }else{
    //servo9.write(90);
    servo2.write(90);
    //servo7.write(90);
  }

}
