const int PIN_Y=1;
const int PIN_SW = 2;    
const int UP_TH   = 300;   
const int DOWN_TH = 700;   

bool lastUp   = false;
bool lastDown = false;
bool lastSw   = false;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_SW, INPUT_PULLUP);   
}

void loop() {
  int y = analogRead(PIN_Y);
  bool sw = (digitalRead(PIN_SW) == LOW);

  bool up   = (y < UP_TH);
  bool down = (y > DOWN_TH);

  //送信
  if (up   && !lastUp)   Serial.println(0);
  if (down && !lastDown) Serial.println(1);
  if (sw   && !lastSw)   Serial.println(2);

  lastUp   = up;
  lastDown = down;
  lastSw   = sw;

  delay(10);
}

