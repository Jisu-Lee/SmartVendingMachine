int coinslot = 7;
int coin_state = 0; int btn2state = 0;

void setup() 
{ 
  pinMode(coinslot, INPUT);
  Serial.begin(9600);
} 
void loop() 
{ 
  btn1state = digitalRead(coinslot);
  Serial.print("coin_state = ");
  Serial.println(coin_state);
  
} 
