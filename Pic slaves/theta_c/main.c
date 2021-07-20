#include <16F877A.h>

#FUSES NOWDT                    //No Watch Dog Timer
#FUSES NOBROWNOUT               //No brownout reset
#FUSES NOLVP                    //No low voltage prgming, B3(PIC16) or B5(PIC18) used for I/O

#use delay(crystal=8Mhz)
#use rs232(baud=9600,parity=N,xmit=PIN_C6,rcv=PIN_C7,bits=8,stream=PORT1)
#use i2c(Slave,sda=PIN_C4,scl=PIN_C3,force_hw,address=0x24)
#use fast_io(B)


#define pi 3.14159
  #define kp 20
   #define ki 0
    #define kd 0
    #define dt 0.01 //100 HZ

signed int16 start_point=0;
float encoder_value=8400;
 signed long int counter = 0; 
 int aState;
 int aLastState;  
 float pwmOut;
 float senPosition=0;
long  set_point=0;
float error,total_error=0;
float prev_error=0;

 byte buffer[4];
 int8 state; 
 long x_1;
 long  x_2;
byte deneme[4];
int16 sayi_1=0;
int16 sayi_2=0;
 
 #define outputA PIN_B4
 #define outputB PIN_B5
#INT_RB                                      // RB port interrupt on change
void RB_IOC_ISR(void) 
{disable_interrupts(INT_SSP);
   aState = input(outputA); 
   if (aState != aLastState){
     
     if (input(outputB)  != aState) {
       counter ++;
     } else {
       counter --;
     }} aLastState = aState;
     
     enable_interrupts(INT_SSP);
}
#INT_SSP
void  SSP_isr(void) 
{
   state = i2c_isr_state();

   if((state== 0 ) || (state== 0x80))

   {  i2c_read();}

   if(state >= 0x80)

    {  i2c_write(deneme[state-0x80]);}

   else if(state > 0)

    {  buffer[state - 1] = i2c_read();}
}

void main()
{
 port_b_pullups(TRUE);
   enable_interrupts(GLOBAL);
   clear_interrupt(INT_RB);
  enable_interrupts(INT_SSP);
 
 setup_timer_2(T2_DIV_BY_16,255,1);
set_tris_d(0x00); 
output_high(pin_d1);
 output_low(pin_d0);

   setup_ccp1(CCP_PWM);
   setup_ccp2(CCP_PWM);
set_pwm1_duty((int16)0);
set_pwm2_duty((int16)0);

deneme[1]=sayi_1 & 0xff;
deneme[0]=(sayi_1 >> 8);
deneme[3]=sayi_2 & 0xff;
deneme[2]=(sayi_2 >> 8);
 while(input(PIN_B7)){
 set_pwm2_duty(20);
  set_pwm1_duty(20);
 }
 start_point=-35;
   enable_interrupts(INT_RB);
   while(TRUE)
   {
    x_1=buffer[0];
      x_1=x_1<<8;
      x_1=x_1 & 0xFF00;
      x_1=x_1 | buffer[1];
      set_point=x_1;
       x_2=buffer[2];
      x_2=x_2<<8;
      x_2=x_2 & 0xFF00;
      x_2=x_2 | buffer[3];
//set_point=90;
   senPosition=4*pi*(counter/encoder_value);
     senPosition=(180*senPosition)/pi+start_point;
      error= set_point-senPosition-500;
      
      sayi_2=senPosition;
deneme[1]=sayi_1 & 0xff;
deneme[0]=(sayi_1 >> 8);
deneme[3]=sayi_2 & 0xff;
deneme[2]=(sayi_2 >> 8);
      
     
      total_error=total_error+error*(ki);
  
      if(total_error>1000){total_error=1000;}
 
      if(total_error<-1000){total_error=-1000;}
 
      pwmOut=kp*(error)+(dt*total_error)+(prev_error-error)*(1/dt)*kd;
  
      prev_error=error;
      
 sayi_1=set_point;
      if(pwmOut>255){pwmOut=255;}
  
      if(pwmOut<-255){pwmOut=-255;}
if(pwmOut>0){
 //digitalWrite(en2, HIGH);
 output_high(pin_d1);
 output_low(pin_d0);
//set_pwm2_duty(0);
    set_pwm1_duty((int8)(pwmOut));
    set_pwm2_duty((int8)(pwmOut));
}
 

if(pwmOut<0){
//digitalWrite(en2, LOW);
pwmOut=-1*pwmOut;
output_high(pin_d0);
 output_low(pin_d1);
set_pwm2_duty((int8)(pwmOut/1.2));
set_pwm1_duty((int8)(pwmOut/1.2));
    //set_pwm1_duty(0);  
    
    }
//printf("%ld \n",(int16)pwmOut);
   //delay_ms (5);

    
    }
  

}

