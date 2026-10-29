// コイン検出とタイマー

const int left = A1;
const int center = A2;
const int right = A3;
const int stick1 = A4;
const int stick2 = A5;
const int coin = 2;

int init1, init2;

const unsigned long timelimit = 60 * 1000;
unsigned long timer = 0;
unsigned long past;
volatile bool isCoined = false;
int activeReel = 3;

void setup() {
  Serial.begin(9600);
  pinMode(left, INPUT_PULLUP);
  pinMode(center, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  pinMode(coin, INPUT_PULLUP);
  init1 = analogRead(stick1);
  init2 = analogRead(stick2);
  attachInterrupt(digitalPinToInterupt(coin), 
                  [](){
                    isCoined = true;
                    timer = timelimit;
                    activeReel = 3;
                  }, FALLING);
}

void loop() {
  String command = "";
  if (isCoined) {
    if (isRolling) {
      if (!digitalRead(left)) {
        // Serial.println("L");
        command = "L";
        activeReel--;
      }
      else if (!digitalRead(center)) {
        // Serial.println("C");
        command = "C";
        activeReel--;
      }
      else if (!digitalRead(right)) {
        // Serial.println("R");
        command = "R";
        activeReel--;
      }
      if (!activeReel) {
        isRolling = false;
      }

      unsigned long current = millis();
      timer -= current - past;
      past = current;
      if(timer <= 0) {
        // Serial.println("T");
        command = "T";
        activeReel = 0;
        isRolling = false;
      }
    }
    else if (activeReel && (abs(analogRead(stick1)-init1) > 5 || abs(analogRead(stick2)-init2) > 5)) {
      // Serial.println("S");
      command = "S";
      isCoined = false;
      past = millis();
      isRolling = true;
    }
  }
  Serial.println(command);
}