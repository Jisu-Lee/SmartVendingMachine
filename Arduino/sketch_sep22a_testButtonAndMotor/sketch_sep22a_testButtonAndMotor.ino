#include <Servo.h> //서보 라이브러리를 불러옵니다.
 
Servo sOne, sTwo, sThree, sFour;  // 서보를 제어할 서보 오브젝트를 만듭니다.
int btn1 = 13; int btn2 = 9;
int btn1state = 0; int btn2state = 0;
int pos = 0;     // 서보 위치를 저장할 변수를 선언합니다.

void setup() 
{ 
  pinMode(btn1, INPUT);
  sOne.attach(2);  // 핀 9의 서보를 서보 오브젝트에 연결합니다.
  Serial.begin(9600);
} 
void loop() 
{ 
  btn1state = digitalRead(btn1);
  Serial.print("button1 = ");
  Serial.println(btn1state);
  
  if(btn1state == LOW){
    sOne.write(0);
    delay(15);
  } else{ sOne.write(90);}
} 
