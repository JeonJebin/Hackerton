#include <SoftwareSerial.h>
#include <DFPlayer_Mini_Mp3.h>
#include <stdlib.h>
char temp;
int rnd=0;
int file=0;
SoftwareSerial mySerial(10, 11); // RX, TX
void setup () {
 Serial.begin (9600);
 mySerial.begin (9600);
 mp3_set_serial (mySerial); // DFPlayer-mini mp3 module 시리얼 세팅
 delay(1); // 볼륨값 적용을 위한 delay
 mp3_set_volume (30); // 볼륨조절 값 0~30
 pinMode(5,OUTPUT);
 pinMode(6,OUTPUT);
 pinMode(7,OUTPUT); 

}
void loop (){ 
 digitalWrite(5,HIGH);
 digitalWrite(6,HIGH);
 digitalWrite(9,HIGH);
 //while (Serial.available() > 0){
  temp=Serial.read();
  rnd=rand()%4;
  
  if (temp=='a'){
  mp3_play (1+8*rnd); //0001 파일 플레이
  delay (1000);
  }
  
  if (temp=='b'){
  mp3_play (2+8*rnd); //0001 파일 플레이
  delay (1000);
  }
  
  if (temp=='c'){
  mp3_play (3+8*rnd); //0001 파일 플레이
  delay (1000);
  }
  
  if (temp=='d'){
  mp3_play (4+8*rnd); //0001 파일 플레이
  delay (1000);
  }
   
  if (temp=='e'){
  mp3_play (5+8*rnd); //0001 파일 플레이
  delay (1000);
  }
  
  if (temp=='f'){
  mp3_play (6+8*rnd); //0001 파일 플레이
  delay (1000);
  }
   
  if (temp=='g'){
  mp3_play (7+8*rnd); //0001 파일 플레이
  delay (1000);
  }
  
  if (temp=='h'){
  mp3_play (8+8*rnd); //0001 파일 플레이
  delay (1000);
  }

  rnd==0;
}
