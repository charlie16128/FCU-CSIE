#include <stdio.h> 
#include "NUC100Series.h" 
#include "MCU_init.h" 
#include "SYS_init.h" 
#include "Seven_Segment.h" 
#include "Scankey.h" 
 
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

		uint16_t i; 
	 
    SYS_Init(); 
 
    OpenSevenSegment(); 
	  OpenKeyPad(); 
		 
		while(1) { 
			i=ScanKey(); 
			 
			if(i >= 1 && i <= 6){ 
				while(ScanKey() == i){
					Display_7seg(num);
				}
				
				if(num <= 1000){
					num = num * 10 + i;
				
				}
			}else if(i == 7){ 
				while(ScanKey() == 7){
					Display_7seg(num);
				}
				
				if(num > 0){
					num = num / 10;
				}
			}
			
			Display_7seg(num);
	  } 
}
