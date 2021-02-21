#define rA 9
#define rK1 10
#define rK2 11
#define lA 4
#define lK1 5
#define lK2 6




void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(rA,OUTPUT);
pinMode(rK1,OUTPUT);
pinMode(rK2,OUTPUT);
pinMode(lA,OUTPUT);
pinMode(lK1,OUTPUT);
pinMode(lK2,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if (Serial.available()>0){
    char data = Serial.read();
    
    if (data=='A') //Forward Condition
      {
       
       right_rotation();
      }
    else if (data=='B')//Reverse ConEdition
      {
        
        left_rotation();
      }
    else if (data=='C')//Clockwise Rotation Condition 
      {
       forward();
      }
    else if (data=='D')//Counter Clockwise Rotation Condition
      {
        backward();
      }
    else if (data=='E')
      {
       stop_();
      }
  }
}


void forward(){

Motor(rA,rK1,rK2,180,true,"Right");
Motor(lA,lK1,lK2,180,false,"Left");
}

void backward(){
Motor(rA,rK1,rK2,180,false,"Right");
Motor(lA,lK1,lK2,180,true,"Left");

}

void right_rotation(){
Motor(rA,rK1,rK2,180,false,"Right");
Motor(lA,lK1,lK2,180,false,"Left");

}
void left_rotation(){
Motor(rA,rK1,rK2,180,true,"Right");
Motor(lA,lK1,lK2,180,true,"Left");

}

void stop_(){

Motor(rA,rK1,rK2,0,false,"Right");
Motor(lA,lK1,lK2,0,true,"Left");
}


void Motor(int pinA, int pinK1, int pinK2,int pwm, bool Clockwise , String motor)
{
 if (pwm>0){ 
  digitalWrite(pinA,HIGH);
 }
 else
 {
 digitalWrite(pinA,LOW);
 }
  if (motor=="Left")
    {
       if (Clockwise==false)
         {
           digitalWrite(pinK1,HIGH);
           analogWrite(pinK2,255-pwm);
         }
      else if (Clockwise==true)
        {
           digitalWrite(pinK2,HIGH);
           analogWrite(pinK1,255-pwm);
        }
          
    }
  else if (motor=="Right")
    {
     if (Clockwise==true)
         {
           digitalWrite(pinK1,HIGH);
           analogWrite(pinK2,255-pwm);
         }
      else if (Clockwise==false)
        {
           digitalWrite(pinK2,HIGH);
           analogWrite(pinK1,255-pwm);
        }
    }
    

}
