//
// GPIO_LED : GPIO output to control an on-board red LED
// 
// EVB : Nu-LB-NUC140
// MCU : NUC140VE3CN

// low-active output control by GPC12

#include <stdio.h>
#include "NUC100Series.h"
#include "MCU_init.h"
#include "SYS_init.h"

int main(void)
{
    SYS_Init(); 
    GPIO_SetMode(PC, BIT12, GPIO_MODE_OUTPUT);
		
		while(1){
		int count = 0;
    while(count < 3){
				PC12 = 0;
				CLK_SysTickDelay(100000);
				PC12 = 1;
				CLK_SysTickDelay(100000);
				PC13 = 0;
				CLK_SysTickDelay(100000);
				PC13 = 1;
				CLK_SysTickDelay(100000);
				PC14 = 0;
				CLK_SysTickDelay(100000);
				PC14 = 1;
				CLK_SysTickDelay(100000);
				PC15 = 0;
				CLK_SysTickDelay(100000);
				PC15 = 1;
				CLK_SysTickDelay(100000);
				count++;
		}
		
		while(count > 0){
				PC15 = 0;
				CLK_SysTickDelay(100000);
				PC15 = 1;
				CLK_SysTickDelay(100000);
				PC14 = 0;
				CLK_SysTickDelay(100000);
				PC14 = 1;
				CLK_SysTickDelay(100000);
				PC13 = 0;
				CLK_SysTickDelay(100000);
				PC13 = 1;
				CLK_SysTickDelay(100000);
				PC12 = 0;
				CLK_SysTickDelay(100000);
				PC12 = 1;
				CLK_SysTickDelay(100000);
				count--;
		}
	}
		 
}
