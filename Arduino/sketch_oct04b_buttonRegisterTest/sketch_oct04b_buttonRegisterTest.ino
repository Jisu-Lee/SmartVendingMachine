#define NUMBER_OF_SHIFT_CHIPS   1     /* Width of data (how many ext lines).*/
#define DATA_WIDTH   NUMBER_OF_SHIFT_CHIPS * 8  /* Width of pulse to trigger the shift register to read and latch.*/
#define PULSE_WIDTH_USEC   5   /* Optional delay between shift register reads.*/
#define POLL_DELAY_MSEC   1000 /* You will need to change the "int" to "long" If the NUMBER_OF_SHIFT_CHIPS is higher than 2.*/
#define BYTES_VAL_T unsigned int

int ploadPin        = 8;  // Connects to Parallel load pin the 165
int clockEnablePin  = 9;  // Connects to Clock Enable pin the 165
int dataPin         = 11; // Connects to the Q7 pin the 165
int clockPin        = 12; // Connects to the Clock pin the 165

BYTES_VAL_T pinValues;
BYTES_VAL_T oldPinValues;

const char tx=1;
int btn1state = 0; 
const char button = 13;

void setup() {
  Serial.begin(9600);

  
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

  pinMode(button, INPUT);
  pinMode(tx, OUTPUT);

  on_off_motor(0,1);

}

void loop() {
  pinValues = read_shift_regs();

  if(pinValues != oldPinValues)
  {
      //Serial.print("*Pin value change detected*\r\n");
      display_pin_values();
      oldPinValues = pinValues;
  }
  delay(POLL_DELAY_MSEC);
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
void display_pin_values()
{
    Serial.print("Pin States:\r\n");

    for(int i = 0; i < DATA_WIDTH; i++)
    {
        Serial.print("  Pin-");
        Serial.print(i);
        Serial.print(": ");

        if((pinValues >> i) & 1){
          Serial.print("HIGH");
          set_ch_pos_spd(i+1, 3850, 50);
        }
        else{
          Serial.print("LOW");
          set_ch_pos_spd(i+1, 400, 50);
        }
        Serial.print("\r\n");
    }

    Serial.print("\r\n");
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
