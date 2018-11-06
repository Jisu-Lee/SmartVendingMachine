#include <Wire.h>  // Comes with Arduino IDE
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

#define NUMBER_OF_SHIFT_CHIPS   1     /* Width of data (how many ext lines).*/
#define DATA_WIDTH   NUMBER_OF_SHIFT_CHIPS * 8  /* Width of pulse to trigger the shift register to read and latch.*/
#define PULSE_WIDTH_USEC   5   /* Optional delay between shift register reads.*/
#define POLL_DELAY_MSEC   1000 /* You will need to change the "int" to "long" If the NUMBER_OF_SHIFT_CHIPS is higher than 2.*/
#define BYTES_VAL_T unsigned int

#define SPRING_DELAY 500

#define SPRING_COUNTER_CLOCK 180
#define SPRING_CLOCK 0

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  // Set the LCD I2C address

int ploadPin        = 8;  // Connects to Parallel load pin the 165
int clockEnablePin  = 9;  // Connects to Clock Enable pin the 165
int dataPin         = 11; // Connects to the Q7 pin the 165
int clockPin        = 12; // Connects to the Clock pin the 165

int servo_1_pin  = 6; // 서보모터
int servo_2_pin  = 2; // 서보모터
int servo_3_pin  = 3; // 서보모터
int servo_6_pin  = 4; // 서보모터
int servo_7_pin  = 10;// 서보모터
int servo_9_pin  = 5; // 서보모터

int coin_pin     = 7; // 코인슬롯

BYTES_VAL_T pinValues;
BYTES_VAL_T oldPinValues;

const char tx=1;
int btn_nine_state = 0; 
const char btn_nine_pin = 13;

int coinCounter = 0;
int coin_state = 0;
int last_coin_state = 0;

Servo servo_1, servo_2, servo_3, servo_6, servo_7, servo_9;

void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);   // initialize the lcd for 16 chars 2 lines, turn on backlight
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Cosmetics");
  lcd.setCursor(0,1);
  lcd.print("Vending Machine");
  delay(1000);  
  
  /* Initialize our digital pins...*/
  pinMode(ploadPin, OUTPUT);
  pinMode(clockEnablePin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, INPUT);

  digitalWrite(clockPin, LOW);
  digitalWrite(ploadPin, HIGH);

  /* Read in and display the pin states at startup.*/
  pinValues = read_shift_regs();
  display_pin_values();
  oldPinValues = pinValues;

  pinMode(btn_nine_pin, INPUT);
  pinMode(tx, OUTPUT);

  on_off_motor(0,1);
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  servo_3.attach(servo_3_pin);
  servo_6.attach(servo_6_pin);
  servo_7.attach(servo_7_pin);
  servo_9.attach(servo_9_pin);

  allStop();
  Serial.println("Set Finish");
  Serial.println("Please Insert the Coin");

  lcd.setCursor(0,0);
  lcd.print("Please       ");
  lcd.setCursor(0,1);
  lcd.print("insert coin : ");
  lcd.print(coinCounter/2);
}

void loop() {
  coin_state = digitalRead(coin_pin);
  if(coin_state != last_coin_state){
    if(coin_state == LOW){
      coinCounter += 2; // one for rotate, one for stop
      Serial.print("coin count = ");
      Serial.println(coinCounter);
      
      lcd.setCursor(0,1);
      lcd.print("insert coin : ");
      lcd.print(coinCounter/2);
    }
    delay(50);
    last_coin_state = coin_state;
  }

//  ---------------coin detected-----------------
  if(coinCounter >= 1){
    btn_nine_state = digitalRead(btn_nine_pin);
    
    if(btn_nine_state == LOW){
      coinCounter--;
      Serial.print("coin count = ");
      Serial.println(coinCounter);
   
      delay(150);
      servo_3.write(180);
      delay(1000);  // 3번째 모터가 돌아가는 시간
      coinCounter--;
      Serial.print("coin count = ");
      Serial.println(coinCounter);
      lcd.setCursor(0,1);
      lcd.print("insert coin : ");
      lcd.print(coinCounter/2);
      
      servo_3.write(90);

      if(coinCounter == 0){
         Serial.println("Please Insert the Coin");
      }
    }
    pinValues = read_shift_regs();
  
    if(pinValues != oldPinValues){
      coinCounter--;
      Serial.print("coin count = ");
      Serial.println(coinCounter);
      lcd.setCursor(0,1);
      lcd.print("insert coin : ");
      lcd.print(coinCounter/2);
      
      display_pin_values();
      oldPinValues = pinValues;
      if(coinCounter == 0){
        Serial.println("Please Insert the Coin");
      }
    }  
    delay(POLL_DELAY_MSEC);
  }
}
void allStop(){
  servo_1.write(90);
  servo_2.write(90);
  servo_3.write(90);
  servo_6.write(90);
  servo_7.write(90);
  servo_9.write(90);
  set_ch_pos_spd(4, 3850, 50);
  set_ch_pos_spd(5, 3850, 50);
  set_ch_pos_spd(8, 3850, 50);
}
/*for button register*/
BYTES_VAL_T read_shift_regs()
{
  long bitVal;
  BYTES_VAL_T bytesVal = 0;

  /* Trigger a parallel Load to latch the state of the data lines,
  */
  digitalWrite(clockEnablePin, HIGH);
  digitalWrite(ploadPin, LOW);
  delayMicroseconds(PULSE_WIDTH_USEC);
  digitalWrite(ploadPin, HIGH);
  digitalWrite(clockEnablePin, LOW);

  /* Loop to read each bit value from the serial out line
   * of the SN74HC165N.
  */
  for(int i = 0; i < DATA_WIDTH; i++)
  {
    bitVal = digitalRead(dataPin);

    /* Set the corresponding bit in bytesVal.
    */
    bytesVal |= (bitVal << ((DATA_WIDTH-1) - i));

    /* Pulse the Clock (rising edge shifts the next bit).
    */
    digitalWrite(clockPin, HIGH);
    delayMicroseconds(PULSE_WIDTH_USEC);
    digitalWrite(clockPin, LOW);
  }
  return(bytesVal);
}

/* Dump the list of zones along with their current status.
*/
void display_pin_values(){
  for(int i = 0; i < DATA_WIDTH; i++){
    int channel = i+1;
       
    if((pinValues >> i) & 1){     
      if(channel == 1){  servo_7.write(90);  }
      else if(channel == 2){  servo_6.write(90);  }
      else if(channel == 3){  set_ch_pos_spd(5, 3850, 50);  }
      else if(channel == 4){  set_ch_pos_spd(8, 3850, 50);  }
      else if(channel == 5){  set_ch_pos_spd(4, 3850, 50);  }
      else if(channel == 6){  servo_9.write(90);  }
      else if(channel == 7){  servo_1.write(90);  }
      else if(channel == 8){  servo_2.write(90);  }  
    }
    else{
      if(channel == 1){  
        servo_7.write(SPRING_COUNTER_CLOCK);
        delay(SPRING_DELAY);  
      }
      else if(channel == 2){ 
        servo_6.write(SPRING_COUNTER_CLOCK);
        delay(SPRING_DELAY);
      }
      else if(channel == 3){  set_ch_pos_spd(5, 7300, 50);  }
      else if(channel == 4){  set_ch_pos_spd(8, 400, 50);  }
      else if(channel == 5){  set_ch_pos_spd(4, 7300, 50);  }
      else if(channel == 6){  
        servo_9.write(SPRING_COUNTER_CLOCK);
        delay(SPRING_DELAY);  
      }
      else if(channel == 7){  
        servo_1.write(SPRING_COUNTER_CLOCK);
        delay(SPRING_DELAY);
      }
      else if(channel == 8){  
        servo_2.write(SPRING_COUNTER_CLOCK);
        delay(SPRING_DELAY);
      }
    }
  }
}

/*for motor expand module*/
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
