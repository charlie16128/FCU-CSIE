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
		int j;
		uint16_t i;
	
    SYS_Init();
	
		GPIO_SetMode(PC, BIT12, GPIO_MODE_OUTPUT); // idk what is this
	
    OpenSevenSegment();
		OpenKeyPad();
	
 	  while(1){
				i=ScanKey();
				if(i == 1){ //D1349111 light Run
					PC12=1; PC13=1; PC14=1; PC15=0;
					CLK_SysTickDelay(300000); // 0.3s
					PC12=1; PC13=1; PC14=0; PC15=0;
					CLK_SysTickDelay(300000);
					PC12=1; PC13=0; PC14=1; PC15=1;
					CLK_SysTickDelay(300000);
					PC12=0; PC13=1; PC14=1; PC15=0;
					CLK_SysTickDelay(300000);
					PC12=1; PC13=1; PC14=1; PC15=0;
					CLK_SysTickDelay(300000);
					PC12=1; PC13=1; PC14=1; PC15=0;
					CLK_SysTickDelay(300000);
					PC12=1; PC13=1; PC14=1; PC15=0;
				}
				if(i == 3){ // 0000 0001 0010 0100 1000 1001 1010 1100 1101 1110 1111
					PC12=1; PC13=1; PC14=1; PC15=0;
					CLK_SysTickDelay(300000);
					
					PC12=1; PC13=1; PC14=0; PC15=1;
					CLK_SysTickDelay(300000);

					PC12=1; PC13=0; PC14=1; PC15=1;
					CLK_SysTickDelay(300000);


					PC12=0; PC13=1; PC14=1; PC15=1;
					CLK_SysTickDelay(300000);

					PC12=0; PC13=1; PC14=1; PC15=0;
					CLK_SysTickDelay(300000);

					PC12=0; PC13=1; PC14=0; PC15=1;
					CLK_SysTickDelay(300000);

					PC12=0; PC13=0; PC14=1; PC15=1;
					CLK_SysTickDelay(300000);

					PC12=0; PC13=0; PC14=1; PC15=0;
					CLK_SysTickDelay(300000);

					PC12=0; PC13=0; PC14=0; PC15=1;
					CLK_SysTickDelay(300000);

					for(j=0; j<2; j++){
							PC12=0; PC13=0; PC14=0; PC15=0;
							CLK_SysTickDelay(300000);

							PC12=1; PC13=1; PC14=1; PC15=1;
							CLK_SysTickDelay(300000);
					}
				}
		}
}
