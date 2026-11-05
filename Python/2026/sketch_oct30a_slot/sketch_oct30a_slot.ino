/*
*/
//kuro
// const int pin_l=2;
// const int pin_c=4;
// const int pin_r=3;
// //const int pin_x=;
// const char pin_y[]="A2";  //char str

//chi-pachi
const char pin_l[]="A3";
const char pin_c[]="A4";
const char pin_r[]="A5";
//const int pin_x=;
const char pin_y[]="A2";


unsigned long now_millis;      //符号なし，長い整数

void setup() {
  // put your setup code here, to run once:
  pinMode(pin_l,INPUT_PULLUP);pinMode(pin_c,INPUT_PULLUP);pinMode(pin_r,INPUT_PULLUP);
  pinMode(pin_y,INPUT_PULLUP);
  Serial.begin(9600);
  unsigned long now_millis =millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    //char num=Serial.read();
    int but_l =digitalRead(pin_l);
    int but_c =digitalRead(pin_c);
    int but_r =digitalRead(pin_r);
    //int stick_x=analogRead(pin_x);
    int stick_y=analogRead(pin_y); 


    if(but_l==HIGH)
    {
      Serial.print("l");
    }else if(but_c==HIGH)
    {
      Serial.print("c");
    }else if(but_r==HIGH)
    {
      Serial.print("r");
//    }else if(60000<tim)
//    {
//      Serial.print("stop_all");
    }else if(30<=stick_y||stick_y<=230)
    {
      Serial.print("n");  //のぬ 真ん中
    }else if(230<stick_y || stick_y<30)
    {
      Serial.print("s");
    }else{
      Serial.print("n");  //のぬ
    }


  }
}
