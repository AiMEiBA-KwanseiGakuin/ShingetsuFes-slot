/*
*/
const int pin_l=;
const int pin_c=;
const int pin_r=;
//const int pin_x=;
const int pin_y=;


void setup() {
  // put your setup code here, to run once:
  pinMode(pin_l,INPUT_PULLUP);pinMode(pin_c,INPUT_PULLUP);pinMode(pin_r,INPUT_PULLUP);
  pinMode(pin_y,INPUT_PULLUP);
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    char num=Serial.read();
    int but_l =digitalRead(pin_l);
    int but_c =digitalRead(pin_c);
    int but_r =digitalRead(pin_r);
    //int stick_x=analogRead(pin_x);
    int stick_y=analogRead(pin_y); 


    if(but_l==HIGH)
    {
      Serial.print("stop_l");
    }else if(but_c==HIGH)
    {
      Serial.print("stop_c");
    }else if(but_r==HIGH)
    {
      Serial.print("stop_r");
    else if(60000<tim)
    {
      Serial.print("stop_all")
    }else if(230<stick_y | stick_y<30)
    {
      Serial.print();
    }else{
    }


  }
}
