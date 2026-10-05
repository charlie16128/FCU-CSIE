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

void all_display(uint8_t value){
		CloseSevenSegment();
		ShowSevenSegment(0,value);
		CLK_SysTickDelay(5000);
		
		CloseSevenSegment();
		ShowSevenSegment(1,value);
		CLK_SysTickDelay(5000);
		
		CloseSevenSegment();
		ShowSevenSegment(2,value);
		CLK_SysTickDelay(5000);
		
		CloseSevenSegment();
		ShowSevenSegment(3,value);		
		CLK_SysTickDelay(5000);	
}

//press PB15 will trigger this function 
int interrupt = 0;
void EINT1_IRQHandler(void)
{
    GPIO_CLR_INT_FLAG(PB, BIT15);	// Clear GPIO interrupt flag
		
		interrupt = 1;
}


//from EXTINT sample code 
void Init_EXTINT(void)
{
    // Configure EINT0 pin and enable interrupt by falling edge trigger
    //GPIO_SetMode(PB, BIT14, GPIO_MODE_INPUT);
    //GPIO_EnableEINT0(PB, 14, GPIO_INT_FALLING);
    //NVIC_EnableIRQ(EINT0_IRQn);

    // Configure EINT1 pin and enable interrupt by rising and falling edge trigger
    GPIO_SetMode(PB, BIT15, GPIO_MODE_INPUT);
    GPIO_EnableEINT1(PB, 15, GPIO_INT_RISING); // RISING, FALLING, BOTH_EDGE, HIGH, LOW
    NVIC_EnableIRQ(EINT1_IRQn);

    // Enable interrupt de-bounce function and select de-bounce sampling cycle time
    GPIO_SET_DEBOUNCE_TIME(GPIO_DBCLKSRC_LIRC, GPIO_DBCLKSEL_64);
    //GPIO_ENABLE_DEBOUNCE(PB, BIT14);
    GPIO_ENABLE_DEBOUNCE(PB, BIT15);
}


int main(void)
{
	int num = 0, mode = 0, lastmode = -1, minute = 0, sec = 0, count = 0, timer = 0, lastkey = 0;
	uint16_t i;
	uint8_t value = 16;
	
	SYS_Init();
	Init_EXTINT();
	GPIO_SetMode(PC, BIT12, GPIO_MODE_OUTPUT); // idk what is this
	
	OpenSevenSegment();
	OpenKeyPad();
	
	while(1){
			if(interrupt == 1){
            if(ScanKey()){
                interrupt = 0;
                while(ScanKey()) all_display(value); //wait release key
                continue;
            }

            if(value > 21) value = 16;

            timer = 0;
            while(timer < 50){
                all_display(value);
                timer++;
            }
            value++;
						continue; //skip one time while
			}
			
			i=ScanKey();
			
			if(i == 1 && lastkey == 0){ //start
				mode = 1;
				lastmode = 1;

			}else if(i == 2 && lastkey == 0){ //pause
				mode = 2;
				lastmode = 2;
			}else if(i == 3 && lastkey == 0){ //reset
				mode = 3;
				num = 0;
				count = 0;
			}else if(i == 4 && lastkey == 0){ //add 50s
				mode = 4;
				num += 50;
				
				minute = num / 60;
				sec = num % 60;
			}
			
			lastkey = i;
			minute = num / 60;
			sec = num % 60;
			Display_7seg(minute * 100 + sec);

			
			if(mode == 1){
				count++;
				
				if(count >= 60){
					num++;
					count = 0;
				}
			}else if (mode == 4){
				if(lastmode == 1) mode = 1;
			}
		}
}
