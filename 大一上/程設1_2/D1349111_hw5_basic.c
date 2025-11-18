#include <stdio.h>
#include <string.h>
#include <ctype.h>
#define YEAR 113

int getnum(int input) {
    int total = 0;
    while (input > 0) {
        total = total + input % 10;
        input = input / 10;
    }
    return total;
}

const char* year_of_student_in_school(int first, int second, int year) {
    int year_in_school;
    if (100 + first * 10 + second > year) { //年份大於現在，例如first、second 為96，不可能為民國196年，故為民國96年
        year_in_school = first * 10 + second; 
    } else {
        year_in_school = 100 + first * 10 + second; //年份小於現在，例如first、second 為11，不可能為民國11年，故為民國111年
    }

    int year_diff = year - year_in_school; //學號年份和當前年分的差

    if (year_diff == 0) {   //差為0，當年剛入學
        return "大一新鮮人";
    } 
    else if (year_diff > 0 && year_diff <= 4) {     //差為1~4，入學1~4年
        static char year_level[10];
        snprintf(year_level, sizeof(year_level), "大%d生", year_diff);
        return year_level;
    } 
    else { //>4 延畢
        return "延畢生";
    }
}

int num(int a, int b, int c, int d) { //計算學號3~6位變成數字 1 2 3 4 = 1234
    return a * 1000 + b * 100 + c * 10 + d;
} 

const char* type(int num) {
    if (num >= 0 && num <= 3) {
        return "特殊選材/繁星推薦/海外申請";
    }
    else if (num >= 4 && num < 7) {
        return "申請入學/四技二專徵選";
    }
    else if (num == 8) {
        return "考試入學(分科測驗)";
    }
    return "";
}

void studen_number_analize(char studen_num[8], int year) {
    if (toupper(studen_num[0]) == 'D') {
        printf("你是大學部，%s，第%d位入學，可能使用'%s'方式入學\n",
               year_of_student_in_school(studen_num[1] - '0', studen_num[2] - '0', year),
                num(studen_num[3] - '0', studen_num[4] - '0', studen_num[5] - '0', studen_num[6] - '0'),
               type(studen_num[3] - '0'));
    }
    else if (toupper(studen_num[0]) == 'E') {
        printf("你是進修部，%s，第%d位入學，可能使用'%s'方式入學\n",
               year_of_student_in_school(studen_num[1] - '0', studen_num[2] - '0', year),
               num(studen_num[3] - '0', studen_num[4] - '0', studen_num[5] - '0', studen_num[6] - '0'),
               type(studen_num[3] - '0'));
    }
    else if (toupper(studen_num[0]) == 'M') {
        printf("你是碩士，%s，第%d位入學，可能使用'%s'方式入學\n",
               year_of_student_in_school(studen_num[1] - '0', studen_num[2] - '0', year),
               num(studen_num[3] - '0', studen_num[4] - '0', studen_num[5] - '0', studen_num[6] - '0'),
               type(studen_num[3] - '0'));
    }
    else if (toupper(studen_num[0]) == 'P') {
        printf("你是博士，%s，第%d位入學，可能使用'%s'方式入學\n",
               year_of_student_in_school(studen_num[1] - '0', studen_num[2] - '0', year),
               num(studen_num[3] - '0', studen_num[4] - '0', studen_num[5] - '0', studen_num[6] - '0'),
               type(studen_num[3] - '0'));
    }
}

int main() {
    char studen_number[10];
    int encode[6] = {8, 7, 6, 8, 7, 6}, mutiply_number[100];

    while (printf("請輸入學號 : ") && scanf("%s", studen_number) != EOF) {
        int sum = 0, check_number = -1, input_check_number = studen_number[7] - '0';
        for (int i = 1; i < 7; i++) {
            mutiply_number[i] = (studen_number[i] - '0') * encode[i - 1]; //把學號2~7位分別成876876
            mutiply_number[i] = getnum(mutiply_number[i]);  //把乘完的結果位數相加 ex:123 = 1 + 2 + 3
            sum += mutiply_number[i];   //計算總和 EX 1 + 2 + 3
        }

        check_number = 10 - sum % 10;
        if(check_number == 10){ //檢查碼為10，讓他=0
            check_number = 0;
        }

        // int year;

        // printf("請輸入當前年份(民國) : ");
        // scanf("%d", &year);

        if (input_check_number == check_number) {
            printf("你的學號為真實學號，檢查碼 ""%d = %d""\n", check_number, input_check_number);
            studen_number_analize(studen_number, YEAR);
            printf("可以發放折價券\n");
        }
        else {
            printf("你的學號非真實學號，檢查碼 %d != %d\n", check_number, input_check_number);
            printf("不可以發放折價券\n");
        }
    }
    return 0;
}