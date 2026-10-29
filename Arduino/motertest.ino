const int Pin_in1 = 2; //入力受け取り 
const int Pin_in2 = 3;
const int Pin_in3 = 4;

const int joy_x = A2;
const int joy_y = A3;

int X_POS;
int Y_POS;
int SW_POS;
int SW_PIN;

const int baudrate = 9600; //115200を使うことも多い

int val1;
int val2;
int val3;

void setup(){
  pinMode(Pin_in1,INPUT_PULLUP);
  pinMode(Pin_in2,INPUT_PULLUP);
  pinMode(Pin_in3,INPUT_PULLUP);
  Serial.begin(baudrate);
  
}

void loop(){
  String message = "n";
  val1 = digitalRead(Pin_in1); // HIGH/LOWで入力値を読み取る
	val2 = digitalRead(Pin_in2);
  val3 = digitalRead(Pin_in3);

	if(val1 == LOW){ // 押されたとき
	  //Serial.println("left");
    message = "l";
    delay(100);	
	}
  
  if(val2 == LOW){
    //Serial.println("right");
    message = "r";
    delay(100);
  }
  
  if(val3 == LOW){
    //Serial.println("center");
    message = "c";
    delay(100);
  }

  X_POS = analogRead(joy_x);     // X軸方向のアナログ値を読み取る
  Y_POS = analogRead(joy_y);     // Y軸方向のアナログ値を読み取る
  SW_POS = digitalRead(SW_PIN);  // センタースイッチの状態を読み取る

  if(X_POS > 520 || Y_POS < 480){
      //Serial.println("start");
      message = "s";
  }
  Serial.println(message);
  Serial.flush();
}