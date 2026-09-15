//
// GPIO_Keypad : 3x3 keypad input and control LEDs (or Relays)
//
// EVB : Nu-LB-NUC140
// MCU : NUC140VE3CN

// PA0,1,2,3,4,5 connected to 3x3 Keypad
// PC12,13,14,15 connected to LEDs (or Relays)

#include <stdio.h>
#include "NUC100Series.h"
#include "MCU_init.h"
#include "SYS_init.h"
#include "Scankey.h"

void Init_GPIO(void)
{
	  GPIO_SetMode(PC, BIT12, GPIO_MODE_OUTPUT);
	  GPIO_SetMode(PC, BIT13, GPIO_MODE_OUTPUT);
	  GPIO_SetMode(PC, BIT14, GPIO_MODE_OUTPUT);
	  GPIO_SetMode(PC, BIT15, GPIO_MODE_OUTPUT);
	  PC12=1; PC13=1; PC14=1; PC15=1;
}

void showled(int number)
{
    PC12 = 1;
    PC13 = 1;
    PC14 = 1;
    PC15 = 1;

    if(number == 12) PC12 = 0;
    if(number == 13) PC13 = 0;
    if(number == 14) PC14 = 0;
    if(number == 15) PC15 = 0;
}

int main(void)
{
    int key;
    int mode = 1;     
    int lastmode = 1; 
    int CurrentLed = 12;

    SYS_Init();
    OpenKeyPad();
    Init_GPIO();

    while(1){
        key = ScanKey();

        if(key == 1){
            mode = 1;
            lastmode = 1;
			while(ScanKey() == 1); //wait 
        }else if(key == 2){
            if(mode == 2)
                mode = lastmode;    
            else{
                lastmode = mode;    
                mode = 2;
            }
            while(ScanKey() == 2);//wait
        }else if(key == 3){
            mode = 3;
            lastmode = 3;
			while(ScanKey() == 3);//wait
        }
				
				
        if(mode == 1){
            showled(CurrentLed);

            CurrentLed++;
            if(CurrentLed > 15) CurrentLed = 12;
        }else if(mode == 3){
            showled(CurrentLed);

            CurrentLed--;
            if(CurrentLed < 12) CurrentLed = 15;
        }

        CLK_SysTickDelay(100000);
    }
}
