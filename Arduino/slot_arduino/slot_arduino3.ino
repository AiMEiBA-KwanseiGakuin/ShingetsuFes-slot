// コイン検出

const int left = A1;
const int center = A2;
const int right = A3;
const int stick1 = A4;
const int stick2 = A5;

const int coin = 2;
volatile bool isCoined = false;

void setup() {
  Serial.begin(9600);
  pinMode(left, INPUT_PULLUP);
  pinMode(center, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  pinMode(coin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterupt(coin), [](){isCoined=true;},FALLING);
}

void loop() {
  if (isCoined) {
    //Serial.println("init");
    isCoined = true;
  }
  else {
    if (!digitalRead(left)) {
      Serial.println("left");
    }
    else if (!digitalRead(center)) {
      Serial.println("center");
    }
    else if (!digitalRead(right)) {
      Serial.println("right");
    }

    if (abs(analogRead(stick1)-512) > 10 || abs(analogRead(stick2)-512) > 10) {
      Serial.println("start");
    }
  }
}