//使用说明：5v和GND接到洞洞板上，舵机、蓝牙、风扇、小灯、继电器连到洞洞板上
//          舵机信号线接P20。风扇继电器信号线接P22，小灯继电器信号线接P21，低电平开启
#include <REGX52.H>
#include "Delay.h"
#include "UART.h"
#include "LCD1602.h"
#include "TIMER0.h"

sbit steer1=P2^0;

unsigned int cnt=1,compare=1;
unsigned char  dat=0;//串口接收数据
unsigned char  i=0;
unsigned char  buff[5]=0;
bit  flag_REC=0; 
bit  flag    =0;

void main()
{
	UART_Init();		//串口初始化
	LCD_Init();
	Timer0Init();
	while(1)
	{
		LCD_ShowNum(1,16,compare,1);
		LCD_ShowHexNum(1,1,dat,2);
//		LCD_ShowChar(1,3,dat);
		if(dat%16==1){LCD_ShowString(2,1,"W-on  L-on  S-on");compare=3;P1_0=1;P1_2=1;}//wind light servo
		else if(dat%16==2){LCD_ShowString(2,1,"W-on  L-off S-on");compare=3;P1_0=1;P1_2=1;}
		else if(dat%16==3){LCD_ShowString(2,1,"W-off L-on  S-on");compare=3;P1_0=0;P1_2=1;}
		else if(dat%16==4){LCD_ShowString(2,1,"W-off L-off S-on");compare=3;P1_0=0;P1_2=1;}
		
		else if(dat%16==5){LCD_ShowString(2,1,"W-on  L-on  S-of");compare=1;P1_0=1;P1_2=0;}
		else if(dat%16==6){LCD_ShowString(2,1,"W-on  L-off S-of");compare=1;P1_0=1;P1_2=0;}
		else if(dat%16==7){LCD_ShowString(2,1,"W-off L-on  S-of");compare=1;P1_0=0;P1_2=0;}
		else {LCD_ShowString(2,1,"W-off L-off S-of");compare=1;P1_0=0;P1_2=0;}
		
//		LCD_ShowString(1,6,buff);
		Delay(10);
	}
}

void UART_Routine() interrupt 4
{
    if(RI)
    {
       RI=0;
       dat=SBUF;
       buff[i]=dat;
	}
}

void Timer0_Routine() interrupt 1
{
	TL0 = 0x33;
	TH0 = 0xFE;
	cnt++;
	if(cnt>40){cnt=1;}//20ms
	if(cnt<=compare){steer1=1;}
	else {steer1=0;}
}
