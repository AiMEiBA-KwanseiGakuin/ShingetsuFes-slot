/*
*/
//kuroのスロット
// const int pin_l=2;
// const int pin_c=4;
// const int pin_r=3;
// //const int pin_x=;
// const char pin_y[]="A2";  //char str

//chi-pachi
const int pin_l = A3;//A3
const int pin_c = A4 ;//A4
const int pin_r = A5 ;//A5      A0は整数！！
// const char pin_x[]="A1";
// const char pin_y[]="A2";

unsigned long now_millis;      //符号なし，長い整数

void setup() {
  // put your setup code here, to run once:
  pinMode(pin_l,INPUT_PULLUP);pinMode(pin_c,INPUT_PULLUP);pinMode(pin_r,INPUT_PULLUP);
  // pinMode(pin_x,INPUT_PULLUP);pinMode(pin_y,INPUT_PULLUP);
  Serial.begin(9600);
  unsigned long now_millis =millis();


}

void loop() {
  // put your main code here, to run repeatedly:
  // if(Serial.available()>0)
  // {
    //char num=Serial.read();
    int but_l =digitalRead(pin_l);
    int but_c =digitalRead(pin_c);
    int but_r =digitalRead(pin_r);
    //int stick_x=analogRead(pin_x);
    // int stick_x=analogRead(pin_x);
    // int stick_y=analogRead(pin_y); 


    
    if(but_l==LOW)
    {
      Serial.println("l");
    }else if(but_c==LOW)
    {
      Serial.println("c");
    }else if(but_r==LOW)
    {
      Serial.println("r");
    //    }else if(60000<tim)
    //    {
    // //      Serial.print("stop_all");
    //     }else if(256<stick_y || stick_y<0)
    //     {
    //       Serial.println("s");
    //     }else if(256<stick_x || stick_x<0)
    //     {
    //       Serial.println("s");
    //    }else if(20<=stick_y||stick_y<=236)
    //    {
    //      Serial.println("n");  //のぬ 真ん中
    
    }else{
      Serial.println("n");  //のぬ
    }


  // }
}
