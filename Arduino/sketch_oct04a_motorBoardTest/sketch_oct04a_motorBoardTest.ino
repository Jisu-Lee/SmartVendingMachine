#include <Servo.h> //서보 라이브러리를 불러옵니다.
 
Servo sOne, sTwo, sThree, sFour;  // 서보를 제어할 서보 오브젝트를 만듭니다.
const char tx=1;
const char button = 13;
int btn1state = 0; 

void setup() {
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(tx, OUTPUT);

  on_off_motor(0,1);

}

void loop() {
  btn1state = digitalRead(button);

  if(btn1state == LOW){
    set_ch_pos_spd(1, 400, 50);
    set_ch_pos_spd(3, 400, 50);
    set_ch_pos_spd(5, 400, 50);
    set_ch_pos_spd(7, 400, 50);
  } 
  else{ 
    set_ch_pos_spd(1, 3850, 50);
    set_ch_pos_spd(3, 3850, 50);
    set_ch_pos_spd(5, 3850, 50);
    set_ch_pos_spd(7, 3850, 50);
  }
}

void on_off_motor(unsigned char channel, unsigned char on){
  unsigned char first_byte = 0;
  first_byte = 0b11000000|channel;
  Serial.write(first_byte);
  Serial.write(on);
}

void set_ch_pos_spd(unsigned char channel, unsigned int position, unsigned char velocity){
  unsigned char first_byte = 0;
  unsigned char high_byte = 0;
  unsigned char low_byte = 0;

  first_byte = 0b11100000|channel;
  high_byte = (position>>6) & 0b01111111;
  low_byte = position & 0b00111111;

  Serial.write(first_byte);
  Serial.write(high_byte);
  Serial.write(low_byte);
  Serial.write(velocity);
}
