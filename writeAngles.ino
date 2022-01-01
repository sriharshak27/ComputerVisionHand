#include <Servo.h>


String tcommand;
String icommand;
String mcommand;
String rcommand;
String pcommand;
int t,i,m,r,p;
Servo thumb;
Servo ind;
Servo middle;
Servo ring;
Servo pinky;
int p1=3,p2=5,p3=6,p4=9,p5=10;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  thumb.attach(p1);
  ind.attach(p2);
  middle.attach(p3);
  ring.attach(p4);
  pinky.attach(p5);
 
  thumb.write(45);
  ind.write(45);
  middle.write(45);
  ring.write(45);
  pinky.write(45);
  delay(100);
}

void loop() {
  // put your main code here, to run repeatedly:

    if(Serial.available()){
//
//      pinMode(p1,OUTPUT);
//      pinMode(p2,OUTPUT);
//      pinMode(p3,OUTPUT);
//      pinMode(p4,OUTPUT);
//      pinMode(p5,OUTPUT);


     
      tcommand=Serial.readStringUntil(' ');
      icommand=Serial.readStringUntil(' ');
      mcommand=Serial.readStringUntil(' ');
      rcommand=Serial.readStringUntil(' ');
      pcommand=Serial.readStringUntil(' ');
      Serial.println(tcommand+" "+icommand+" "+ mcommand+" "+rcommand+" "+pcommand);

     
     

     
      t=tcommand.toInt();
      t=map(t,0,90,45,135);

     

      i=icommand.toInt();
//      i=map(i,65,85,45,90);
      i=map(i,45,90,45,135);
      if(i<45)i=45;
      if(i>135)i=135;
     

      m=mcommand.toInt();
//      m=map(m,58,88,45,90);
      m=map(m,45,90,45,135);
      if(m<45)m=45;
      if(m>135)m=135;
     

      r=rcommand.toInt();
//      r=map(r,59,86,45,90);
      r=map(r,45,90,45,135);
      if(r<45)r=45;
      if(r>135)r=135;      
     
       

      p=pcommand.toInt();
//      p=map(p,67,84,45,90);    
      p=map(p,45,90,45,135);
      if(p<45)p=45;
      if(p>135)p=135;

     
      adjust(t,i,m,r,p);
//      delay(200);
//      pinMode(p1,INPUT);
//      pinMode(p2,INPUT);
//      pinMode(p3,INPUT);
//      pinMode(p4,INPUT);
//      pinMode(p5,INPUT);
    }
   
//    else{
//      adjust(70,70,70,70,70);
//    }
}

void adjust(int a,int b,int c,int d,int e){
  thumb.write(a);
  ind.write(b);
  middle.write(c);
  ring.write(d);
  pinky.write(e);
  //delay(100);
}
