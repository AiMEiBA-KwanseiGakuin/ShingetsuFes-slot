// 一番シンプルなやつ

const int left = 2;
const int center = 3;
const int right = 4;
const int stick1 = A3;
const int stick2 = A2;

int init1, init2;

void setup() {
  Serial.begin(9600);
  pinMode(left, INPUT_PULLUP);
  pinMode(center, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  init1 = analogRead(stick1);
  init2 = analogRead(stick2);
}

void loop() {
  if (!digitalRead(left)) {
    Serial.println("left");
  }
  else if (!digitalRead(center)) {
    Serial.println("center");
  }
  else if (!digitalRead(right)) {
    Serial.println("right");
  }

  if (abs(analogRead(stick1)-init1) > 10 || abs(analogRead(stick2)-init2) > 10) {
    Serial.println("start");
  }

}