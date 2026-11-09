// 一番シンプルなやつ

const int left = A3;
const int center = A4;
const int right = A5;
const int stick1 = A1;
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
  String command = "";
  if (!digitalRead(left)) {
    // Serial.println("left");
    command = "l";
  }
  else if (!digitalRead(center)) {
    // Serial.println("center");
    command = "c";
  }
  else if (!digitalRead(right)) {
    // Serial.println("right");
    command = "r";
  }

  if (abs(analogRead(stick1)-init1) > 20 || abs(analogRead(stick2)-init2) > 20) {
    Serial.println("s");
  }

  Serial.println(command);
}