#include <Wire.h>

int x_1;
int x_2;
int x_3;
int x_4;
int x_5;
int x_6;
//
int a=500;
int b=500;
int c=10;
int d=0;
int e=10;
int f=0;
//
uint8_t man_1[4];
uint8_t man_2[4];
uint8_t man_3[4];

//
int con1;
int con2;
int con3;
//
 int count=0;
char strInput[6];
//
void setup()
{
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
  delay(100);
}

void loop()
{
if( Serial.available()>0) // Haberleşmenin olup olmadıgını kontrol eder
  {
    char i = Serial.read(); 
    
 if (i == 'a')
      {
count = 0;

a=atol(strInput)+500;

memset(strInput, 0, 6);
    }
     else if (i == 'b')
      {
count = 0;

b=atol(strInput)+500;

memset(strInput, 0, 6);
    }
     else if (i == 'c')
      {
count = 0;

c=atol(strInput);

memset(strInput, 0, 6);
    }
     else if (i == 'd')
      {
count = 0;

d=atol(strInput);

memset(strInput, 0, 6);
    }

     else if (i == 'e')
      {
count = 0;

e=atol(strInput);

memset(strInput, 0, 6);
    }
     else if (i == 'f')
      {
count = 0;

f=atol(strInput);

memset(strInput, 0, 6);
    }
    
     
     else if (i == 'h')
      {
count = 0;
memset(strInput, 0,6);
//house();
    }
 
          else
      {
         strInput[count] = i;
         count++;
         if(count>7){
          
count = 0;
memset(strInput, 0,6);
          
          }
        
      }
          

  }



  
 delay(100);
    
man_1[1] = a & 0xff;
man_1[0]= (a >> 8);
man_1[3] = b & 0xff;
man_1[2]= (b >> 8);

man_2[1] = c & 0xff;
man_2[0]= (c >> 8);
man_2[3] = d & 0xff;
man_2[2]= (d >> 8);

man_3[1] = e & 0xff;
man_3[0]= (e >> 8);
man_3[3] = f & 0xff;
man_3[2]= (f >> 8);
 //////////////////////////
  Wire.beginTransmission(17); // transmit to device #10
     Wire.write(man_1[0]); 
     Wire.write(man_1[1]); 
    Wire.write(man_1[2]); 
    Wire.write(man_1[3]); 
    con1= Wire.endTransmission();    // stop transmitting
  

    
  Wire.beginTransmission(18); // transmit to device #11
    Wire.write(man_2[0]); 
     Wire.write(man_2[1]); 
    Wire.write(man_2[2]); 
    Wire.write(man_2[3]); 
  con2 =  Wire.endTransmission();    // stop transmittin


      Wire.beginTransmission(19); // transmit to device #11
    Wire.write(man_3[0]); 
     Wire.write(man_3[1]); 
    Wire.write(man_3[2]); 
    Wire.write(man_3[3]); 
   con3=Wire.endTransmission();    // stop transmitting
  
  
  ///////////////////////
  if(con2==0){
  Wire.requestFrom(18, 4);    
  while(Wire.available()< 4) ;   
  x_3 = Wire.read()<<8|Wire.read();                               
   x_4 = Wire.read()<<8|Wire.read();
   Serial.print(8998); 
   Serial.print(x_3+3500); 
    Serial.print(x_4+4500); 
  }else{Serial.print(8999);}

 if(con1==0){  
 Wire.requestFrom(17, 4);    
  while(Wire.available()< 4) ;   
  x_1 = Wire.read()<<8|Wire.read();                               
   x_2 = Wire.read()<<8|Wire.read(); 
   Serial.print(9998); 
   Serial.print(x_1+1500); 
   Serial.print(x_2+2500);  
   }else{Serial.print(9999);}

if(con3==0){  
     Wire.requestFrom(19, 4);    
  while(Wire.available()< 4) ;   
  x_5 = Wire.read()<<8|Wire.read();                               
   x_6 = Wire.read()<<8|Wire.read(); 
   Serial.print(7998);
    Serial.print(x_5+5500); 
    Serial.print(x_6+6500); }
   else{Serial.print(7999);}

 
}
