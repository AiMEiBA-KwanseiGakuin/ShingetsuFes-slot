const int PIN_SW = 2;    // 押し込みボタン

const int UP_TH   = 300;   // これ未満で「上」(向きは配線で逆になることがある)
const int DOWN_TH = 700;   // これより大きいと「下」

bool lastUp   = false;
bool lastDown = false;
bool lastSw   = false;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_SW, INPUT_PULLUP);   // 押すとLOW
}

void loop() {
  int y = analogRead(PIN_Y);
  bool sw = (digitalRead(PIN_SW) == LOW);

  bool up   = (y < UP_TH);
  bool down = (y > DOWN_TH);

  // 倒した瞬間・押した瞬間だけ送信
  if (up   && !lastUp)   Serial.println(0);
  if (down && !lastDown) Serial.println(1);
  if (sw   && !lastSw)   Serial.println(2);

  lastUp   = up;
  lastDown = down;
  lastSw   = sw;

  delay(10);
}

これってどういうこと
