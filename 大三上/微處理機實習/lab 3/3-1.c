//
// GPIO_7seg_keypad : 3x3 keypad inpt and display on 7-segment LEDs
//
#include <stdio.h>
#include "NUC100Series.h"
#include "MCU_init.h"
#include "SYS_init.h"
#include "Seven_Segment.h"
#include "Scankey.h"

// display an integer on four 7-segment LEDs
void Display_7seg(uint16_t value)
{
  uint8_t digit;
	digit = value / 1000;
	CloseSevenSegment();
	ShowSevenSegment(3,digit);
	CLK_SysTickDelay(5000);
			
	value = value - digit * 1000;
	digit = value / 100;
	CloseSevenSegment();
	ShowSevenSegment(2,digit);
	CLK_SysTickDelay(5000);

	value = value - digit * 100;
	digit = value / 10;
	CloseSevenSegment();
	ShowSevenSegment(1,digit);
	CLK_SysTickDelay(5000);

	value = value - digit * 10;
	digit = value;
	CloseSevenSegment();
	ShowSevenSegment(0,digit);
	CLK_SysTickDelay(5000);
}

int main(void)
{
		int num = 0;
		int mode = 0;
		int minute = 0;
		int sec = 0;
		int count = 0;
	
		uint16_t i;
	
    SYS_Init();

    OpenSevenSegment();
	  OpenKeyPad();
		
		while(1) {
			i=ScanKey();
			
			if(i == 1){
				mode = 1;

			}else if(i == 2){
				mode = 2;

			}else if(i == 3){
				mode = 3;
				num = 0;
				count = 0;
			}
			
			minute = num / 60;
			sec = num % 60;
			Display_7seg(minute * 100 + sec);

			
			if(mode == 1){
				count++;
				
				if(count >= 50){
					num++;
					count = 0;
				}
			}
	  }
}	





