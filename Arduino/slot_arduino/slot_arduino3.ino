// コイン検出とタイマー

const int left = A1;
const int center = A2;
const int right = A3;
const int stick1 = A4;
const int stick2 = A5;

const unsigned long timelimit = 60 * 1000;
unsigned long timer = 0;
unsigned long past;

const int coin = 2;
volatile bool isCoined = false;

int activeReel = 3;

void setup() {
  Serial.begin(9600);
  pinMode(left, INPUT_PULLUP);
  pinMode(center, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  pinMode(coin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterupt(coin), [](){isCoined=true;timer=timelimit;activeReel=3;},FALLING);
}

void loop() {
  if (isCoined) {
    if (isRolling) {
      if (!digitalRead(left)) {
        Serial.println("left");
        activeReel--;
      }
      else if (!digitalRead(center)) {
        Serial.println("center");
        activeReel--;
      }
      else if (!digitalRead(right)) {
        Serial.println("right");
        activeReel--;
      }
      if (!activeReel) {
        isRolling = false;
      }

      unsigned long current = millis();
      timer -= current - past;
      past = current;
      if(timer <= 0) {
        Serial.println("timeup");
        activeReel = 0;
        isRolling = false;
      }
    }
    else if (activeReel && (abs(analogRead(stick1)-512) > 10 || abs(analogRead(stick2)-512) > 10)) {
      Serial.println("start");
      isCoined = false;
      past = millis();
    }
  }
}