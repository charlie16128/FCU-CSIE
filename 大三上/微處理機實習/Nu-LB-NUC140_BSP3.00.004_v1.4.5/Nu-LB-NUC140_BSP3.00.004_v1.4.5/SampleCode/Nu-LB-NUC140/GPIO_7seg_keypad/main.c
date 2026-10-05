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

void Display_ERR(void)
{
    int i;

    for(i = 3; i >= 0; i--){
        CloseSevenSegment();

        if(i == 2){
            ShowSevenSegment(i, 14);
        }
        else if(i < 2){
            ShowSevenSegment(i, 14);
            PE2 = 1;
            PE3 = 1;
            PE5 = 1;
        }

        CLK_SysTickDelay(5000);
    }
}

int main(void)
{
    int count = 0, mode = 0, current = 3;
    uint8_t LED[4] = {0, 0, 0, 0}; // if 1000 leftest is seg rightest -> show 0001
    uint8_t answer[4] = {4, 3, 2, 1};
    uint8_t key;
    uint8_t lastKey = 0;
    int i, j, flash, correct;

    SYS_Init();
    OpenSevenSegment();
    OpenKeyPad();

    while(1){
        key = ScanKey();

        if(mode == 0){
            Display_7seg(0);

            if(key == 1){
                count++;

                if(count >= 150){
                    count = 0;
                    current = 3;
                    mode = 1;
                }
            }
            else{
                count = 0;
            }
        }

        // input mode
        else if(mode == 1){
            if(key != 0 && lastKey == 0){
                if(key == 4){
                    current++;
                    if(current > 3) current = 0;
                }

                if(key == 6){
                    current--;
                    if(current < 0) current = 3;
                }

                if(key == 2){
                    if(LED[current] >= 9){
                        LED[current] = 0;
                    }
                    else{
                        LED[current]++;
                    }
                }

                if(key == 8){
                    if(LED[current] < 10 || LED[current] >= 15){
                        LED[current] = 10;
                    }
                    else{
                        LED[current]++;
                    }
                }
            }

            for(i = 0; i <= 3; i++){
                CloseSevenSegment();
                ShowSevenSegment(i, LED[i]);
                CLK_SysTickDelay(5000);
            }
            CloseSevenSegment();

            if(key == 9){ //enter compare mode
                count++;

                if(count >= 150){
                    count = 0;
                    mode = 2;
                }
            }
            else{
                count = 0;
            }
        }

        // compare mode
        else if(mode == 2){
            correct = 1;

            for(i = 0; i < 4; i++){
                if(LED[i] != answer[i]){
                    correct = 0;
                }
            }

            for(flash = 0; flash < 6; flash++){
                for(j = 0; j < 25; j++){
                    if(flash % 2 == 0){
                        if(correct == 1){
                            Display_7seg(7777);
                        }
                        else{
                            Display_ERR();
                        }
                    }
                    else{
                        CloseSevenSegment();
                        CLK_SysTickDelay(20000);
                    }
                }
            }

            CloseSevenSegment();

            for(i = 0; i < 4; i++){
                LED[i] = 0;
            }

            count = 0;
            current = 3;
            mode = 0;
        }

        lastKey = key;
    }
}