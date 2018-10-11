#include <Wire.h>

//Compatible with the Arduino IDE 1.0
//Library version:1.1
#include <LiquidCrystal_I2C.h>          // LCD library

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x20 for a 16 chars and 2 line display

void setup()
{
  lcd.begin();                      // initialize the lcd 
 
  // Print a message to the LCD.
  lcd.backlight();  // turn on backlight
  lcd.print("Hello, world!");
}

void loop()
{
}
