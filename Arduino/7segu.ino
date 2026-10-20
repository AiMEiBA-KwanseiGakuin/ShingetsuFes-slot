// ===== ピン設定 =====
const int COIN_PIN = 11;    // コイン投入スイッチ(INPUT_PULLUP)
const int Seg1_PIN = 12;    // 1桁目(1の位)
const int Seg2_PIN = 13;    // 2桁目(10の位)
const int PIN_X = A0;       // ジョイスティック横
const int PIN_Y = A1;       // ジョイスティック縦

//ジョイスティックのしきい値
const int LOW_TH  = 300;
const int HIGH_TH = 700;

//状態
enum State { S_IDLE, S_COIN, S_COUNTING, S_END };
State state = S_IDLE;

//カウントダウン
int count = 0;                            // 7セグに表示する数字
unsigned long lastTick = 0;               // 最後にカウントを減らした時刻
const unsigned long TICK_MS = 1000;       // 1秒ごとに減らす
const unsigned long END_SHOW_MS = 2000;   // 終了後に0を見せる時間
unsigned long endTime = 0;

bool coinBefore = HIGH;                   // コインスイッチの前回状態

bool reelStop = false;

// LEDレイアウトの配列を定義
boolean number[10][7] = {
  {1,1,1,1,1,1,0},  // 0
  {0,1,1,0,0,0,0},  // 1
  {1,1,0,1,1,0,1},  // 2
  {1,1,1,1,0,0,1},  // 3
  {0,1,1,0,0,1,1},  // 4
  {1,0,1,1,0,1,1},  // 5
  {1,0,1,1,1,1,1},  // 6
  {1,1,1,0,0,0,0},  // 7
  {1,1,1,1,1,1,1},  // 8
  {1,1,1,1,0,1,1}   // 9
};

void setup() {
  Serial.begin(9600);

  for (int i = 2; i <= 8; i++) {
    pinMode(i, OUTPUT);             // D2~D8を出力に
  }

  pinMode(COIN_PIN, INPUT_PULLUP);  // コインスイッチ(押すとLOW)
  pinMode(Seg1_PIN, OUTPUT);
  pinMode(Seg2_PIN, OUTPUT);
}

void loop() {
  // --- PCからの通知(全リール停止) ---
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'S') reelStop = true;
  }

  // --- コインが投入された瞬間を検出 ---
  bool coinNow = digitalRead(COIN_PIN);
  bool coinPressed = (coinBefore == HIGH && coinNow == LOW);
  coinBefore = coinNow;

  // --- ジョイスティックが倒されたか ---
  int x = analogRead(PIN_X);
  int y = analogRead(PIN_Y);
  bool tilted = (x < LOW_TH || x > HIGH_TH || y < LOW_TH || y > HIGH_TH);

  // --- 状態遷移 ---
  switch (state) {
    case S_IDLE:                       // 最初は0を表示
      count = 0;
      if (coinPressed) {
        count = 60;                    // コイン投入で60
        state = S_COIN;
        Serial.println("COIN");
      }
      break;

    case S_COIN:                       // 60表示のまま待機
      if (tilted) {                    // ジョイスティックが倒されたら開始
        state = S_COUNTING;
        lastTick = millis();
        reelStop = false;
        Serial.println("START");
      }
      break;

    case S_COUNTING:                   // 60→0 のカウントダウン
      if (millis() - lastTick >= TICK_MS) {
        lastTick += TICK_MS;
        count--;
      }
      if (count <= 0 || reelStop) {    // 0 または 全リール停止で終了
        if (count < 0) count = 0;
        state = S_END;
        endTime = millis();
        Serial.println("END");
      }
      break;

    case S_END:                        // 少しだけ結果を見せて待機へ戻る
      if (millis() - endTime >= END_SHOW_MS) {
        count = 0;
        state = S_IDLE;
      }
      break;
  }

  // 7セグ表示
  int d1 = count % 10;                 // 1の位
  int d2 = (count / 10) % 10;          // 10の位

  digitalWrite(Seg2_PIN, LOW);         // 2桁目OFF
  digitalWrite(Seg1_PIN, HIGH);        // 1桁目ON
  NumPrint(d1);
  delay(5);

  digitalWrite(Seg1_PIN, LOW);         // 1桁目OFF
  digitalWrite(Seg2_PIN, HIGH);        // 2桁目ON
  NumPrint(d2);
  delay(5);
}

// LED表示関数
void NumPrint(int n) {
  for (int i = 0; i <= 6; i++) {
    digitalWrite(i + 2, !number[n][i]);
  }
}