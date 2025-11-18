#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

void printProgressBar(int progress, int total, int barWidth) {
  printf("[");
  int numberOfBars = (int)(((float)progress / total) * barWidth);

  for (int i = 0; i < barWidth; i++) {
    if (i < numberOfBars) {
      putchar('=');
    } else {
      putchar(' ');
    }
  }

  printf("] 完成進度 : %3.1f %%     距離上次程式設計師節已經 %d / %d 天\r",
         ((float)progress / total) * 100, progress, total);
  fflush(stdout);
}

int leapYear(int y) {
  return ((y % 400 == 0) || ((y % 4 == 0) && !(y % 100 == 0)));
}

int howManyDays(int year, int month) {
  if (year < 0 || month < 1 || month > 12)
    return 0;
  switch (month) {
  case 1:
  case 3:
  case 5:
  case 7:
  case 8:
  case 10:
  case 12:
    return 31;
  case 4:
  case 6:
  case 9:
  case 11:
    return 30;
  case 2:
    return (leapYear(year) ? 29 : 28);
  }
  return 0;
}

typedef struct { //定義新結構 hoilday 為兩int 以便在下面的函式一次回傳兩值
  int month;
  int day;
} Holiday;

Holiday calculate_hoilday(int year) { //找尋輸入年分的程式設計師節是哪天

  Holiday result;                            //定義回傳值
  int hoilday_month = 1, hoilday_date = 256; //初始設定節日為1月,剩下256天
  while (
      hoilday_date >
      howManyDays(
          year,
          hoilday_month)) { //只要剩餘天數還大於下個月天數就繼續減(代表在下個月之後)
    hoilday_date =
        hoilday_date -
        howManyDays(
            year,
            hoilday_month); //例如 256 = 256 - 31 (1月)....應該會減到9月12(2024)
    hoilday_month++;
  }
  result.month = hoilday_month;
  result.day = hoilday_date;
  return result;
}

int how_many_day_between(int year_start, int month_start, int day_start,
                         int year_end, int month_end,
                         int day_end) { //計算日期之間的天數
  int counter = 0;
  if (year_start == year_end) {     //同年
    if (month_start == month_end) { // 同年同月，直接計算天數
      counter = day_end - day_start;
    } else { // 同年不同月
      counter += howManyDays(year_start, month_start) -
                 day_start; // 計算開始月剩餘的天數

      for (int i = month_start + 1; i < month_end;
           i++) { // 計算中間完整月份的天數

        counter += howManyDays(year_start, i);
      }
      counter += day_end; // 計算結束月的天數
    }
  }
  // 不同年
  else {
    counter +=
        howManyDays(year_start, month_start) - day_start; // 開始月剩餘的天數

    for (int i = month_start + 1; i <= 12; i++) { // 計算開始月份+1到12月的天數
      counter += howManyDays(year_start, i);
    }

    for (int i = 1; i < month_end;
         i++) { // 計算結束年份從1月開始到結束月份的天數
      counter += howManyDays(year_end, i);
    }

    counter += day_end; // 加上結束月份的天數
  }
  return counter;
}

void print_progressbar_result(int day_remain) {
  int daypassed = 0;
  while (daypassed < day_remain) {
    daypassed += rand() % 6;

    // 檢查是否超過要顯示天數
    if (daypassed > day_remain) {
      daypassed = day_remain; // 如果超過，則設為最大值
    }

    printProgressBar(daypassed, 365, 40);
    usleep(20000); // pause 0.2秒

    for (int i = 0; i < 40 + 10; i++) {
      putchar('\b');
    }
  }
}

int main() {
  printf("請輸入當前的年 / 月 / 日\n");
  int year, month, date;
  scanf("%d %d %d", &year, &month, &date);

  Holiday Programmer_day =
      calculate_hoilday(year); //呼叫函示找尋當年的程式設計師節是幾號
  Holiday programmer_day_next_year =
      calculate_hoilday(year + 1); //呼叫函示找尋隔年的程式設計師節是幾號

  //判斷節日過了/剛好同天/還沒到
  if (Programmer_day.month > month ||
      (Programmer_day.month == month &&
       Programmer_day.day > date)) { //節日比當前時間晚(還沒到)

    int counter =
        how_many_day_between(year, month, date, year, Programmer_day.month,
                             Programmer_day.day); //計算今年節日距離現在的天數

    print_progressbar_result(365 -
                             counter); //給progressbar要顯示的數字(過了幾天)
    printf("\n");

    printf("今年的程式設計師節還沒到，在 %d 月 %d 日\n還剩下 %d 天",
           Programmer_day.month, Programmer_day.day, counter);
  } else if (Programmer_day.month == month &&
             Programmer_day.day == date) { //節日恰同天
    print_progressbar_result(365); //給progressbar要顯示的數字(過了幾天)
    printf("\n");
    printf("今天正好是程式設計師節 %d 年 %d 月 %d 日", year,
           Programmer_day.month, Programmer_day.day);
  } else if (Programmer_day.month < month ||
             (Programmer_day.month == month &&
              Programmer_day.day < date)) { //節日比當前時間早(過了)

    int counter = how_many_day_between(
        year, month, date, year + 1, programmer_day_next_year.month,
        programmer_day_next_year.day); //計算明年節日距離現在的天數

    print_progressbar_result(365 -
                             counter); //給progressbar要顯示的數字(過了幾天)

    printf("\n");

    printf("今年的程式設計師節已經過了，在 %d 月 %d 日,已經過了 %d 天\n",
           Programmer_day.month, Programmer_day.day,
           how_many_day_between(year, Programmer_day.month, Programmer_day.day,
                                year, month, date));
    printf("明年的程式設計師節是 %d 年 %d 月 %d 日，還剩下 %d 天\n", year + 1,
           Programmer_day.month, Programmer_day.day, counter);
  }

  printf("\n");

  return 0;
}