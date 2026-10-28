// タイマー実装

const int left = A1;
const int center = A2;
const int right = A3;
const int stick1 = A4;
const int stick2 = A5;

const unsigned long timelimit = 60 * 1000;
unsigned long timer = 0;
unsigned long past;

void setup() {
  Serial.begin(9600);
  pinMode(left, INPUT_PULLUP);
  pinMode(center, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  timer = timelit;
  past = millis();
}

void loop() {
  if(timer) {
    if (!digitalRead(left)) {
      Serial.println("left");
    }
    else if (!digitalRead(center)) {
      Serial.println("center");
    }
    else if (!digitalRead(right)) {
      Serial.println("right");
    }
    unsigned long current = millis();
    timer -= current - past;
  }
  else {
    Serial.println("timeup");
  }
  if (abs(analogRead(stick1)-512) > 10 || abs(analogRead(stick2)-512) > 10) {
    Serial.println("start");
    timer = timelimit;
  }
}