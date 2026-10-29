// タイマー実装

const int left = A1;
const int center = A2;
const int right = A3;
const int stick1 = A4;
const int stick2 = A5;

int init1, init2;

const unsigned long timelimit = 60 * 1000;
unsigned long timer = 0;
unsigned long past;

void setup() {
  Serial.begin(9600);
  pinMode(left, INPUT_PULLUP);
  pinMode(center, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  init1 = analogRead(stick1);
  init2 = analogRead(stick2);
  timer = timelimit;
  past = millis();
}

void loop() {
  String command = "";
  if(timer) {
    if (!digitalRead(left)) {
      // Serial.println("left");
      command = "L";
    }
    else if (!digitalRead(center)) {
      // Serial.println("center");
      command = "C";
    }
    else if (!digitalRead(right)) {
      // Serial.println("right");
      command = "R";
    }
    unsigned long current = millis();
    timer -= current - past;
  }
  else {
    // Serial.println("timeup");
    command = "T";
  }
  if (abs(analogRead(stick1)-init1) > 5 || abs(analogRead(stick2)-init2) > 5) {
    // Serial.println("start");
    command = "S";
    timer = timelimit;
  }
  Serial.println(command);
}