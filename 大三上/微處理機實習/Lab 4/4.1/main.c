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

// timer
int count = 0;

//press PB15 will trigger this function 
void EINT1_IRQHandler(void)
{
    GPIO_CLR_INT_FLAG(PB, BIT15);	// Clear GPIO interrupt flag
    //printf("PB15 EINT1 occurred.\n");
		
		while(count <= 100){
			Display_7seg(8501);
			count++;
		}
		CloseSevenSegment();
		count = 0;
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
	uint16_t i;
	
    SYS_Init();
		Init_EXTINT();
		GPIO_SetMode(PC, BIT12, GPIO_MODE_OUTPUT); // idk what is this
	
    OpenSevenSegment();
	
 	  while(1);
}
