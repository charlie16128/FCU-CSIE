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

uint8_t studentID[8] = {13, 1, 3, 4, 9, 1, 1, 1}; //D1349111

void Display_ID(int position)
{
    int j;
    int index;

    for(j = 0; j < 4; j++){
        index = position + j;

        CloseSevenSegment();

        if(index >= 0 && index < 8){
            ShowSevenSegment(3 - j, studentID[index]);
        }

        CLK_SysTickDelay(5000);
    }
}

int main(void)
{
    uint8_t key;
    uint8_t lastKey = 0;

    int position = 0;
    uint8_t finished = 0;

    uint8_t blinkOn = 1;
    uint8_t blinkCount = 0;

    SYS_Init();
    OpenSevenSegment();
    OpenKeyPad();

    while(1){
        key = ScanKey();

        if(key != 0 && lastKey == 0){
            if(key == 5){ // init
                position = 0;
                finished = 0;
                blinkOn = 1;
                blinkCount = 0;
            }
            else if(finished == 0){
                if(key == 4){
                    position++;
                }
                else if(key == 6){
                    position--;
                }

                if(position == 8 || position == -4){
                    finished = 1;
                    blinkOn = 0;
                    blinkCount = 0;
                }
            }
        }

        lastKey = key;

        if(finished == 0){
            Display_ID(position);
        }
        else if(finished == 1){
            if(blinkOn == 1){
                Display_7seg(7777);
            }
            else{
                CloseSevenSegment();
                CLK_SysTickDelay(20000);
            }
						
            blinkCount++;

            if(blinkCount >= 25){ //wait
                blinkCount = 0;
                blinkOn = !blinkOn;
            }
        }
    }
}