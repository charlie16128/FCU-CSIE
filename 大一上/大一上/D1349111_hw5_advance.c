#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define YEAR 113

// 計算各位數和
int getnum(int input) {
    int total = 0;
    while (input > 0) {
        total += input % 10;
        input /= 10;
    }
    return total;
}

// 判斷入學年度
const char* year_of_student_in_school(int first, int second, int year) {
    int year_in_school;
    if (100 + first * 10 + second > year) {//年份大於現在，例如first、second 為96，不可能為民國196年，故為民國96年
        year_in_school = first * 10 + second;
    } else {
        year_in_school = 100 + first * 10 + second;//年份小於現在，例如first、second 為11，不可能為民國11年，故為民國111年
    }
    
    int year_diff = year - year_in_school;//學號年份和當前年分的差
    static char year_level[10];

    if (year_diff == 0) {//差為0，當年剛入學
        return "新鮮人";
    } else if (year_diff > 0 && year_diff <= 4) { //差為1~4，入學1~4年
        snprintf(year_level, sizeof(year_level), "大%d生", year_diff);
        return year_level;
    } else {//>4 延畢
        return "延畢生";
    }
}

//計算學號3~6位變成數字 1 2 3 4 = 1234
int num(int a, int b, int c, int d) { 
    return a * 1000 + b * 100 + c * 10 + d;
}

// 判斷入學方式
const char* type(int num) {
    if (num >= 0 && num <= 3) {
        return "特殊選材/繁星推薦/海外申請";
    } else if (num >= 4 && num < 7) {
        return "申請入學/四技二專徵選";
    } else if (num == 8) {
        return "考試入學(分科測驗)";
    }
    return "";
}

// 檢查學號是否包含特定數字
int contains_digit(const char* student_num, char digit) {
    for (int i = 0; i < strlen(student_num); i++) {
        if (student_num[i] == digit) {
            return 1;
        }
    }
    return 0;
}

// 獲取當前星期幾
int get_day_of_week() {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    return tm.tm_wday;
}

// 分析學號並提供行銷優惠
void student_number_analyze(char student_num[8], int year) {
    const char* education_level;
    if (toupper(student_num[0]) == 'D') {
        education_level = "大學部";
    } else if (toupper(student_num[0]) == 'E') {
        education_level = "進修部";
    } else if (toupper(student_num[0]) == 'M') {
        education_level = "碩士";
    } else if (toupper(student_num[0]) == 'P') {
        education_level = "博士";
    } else {
        education_level = "未知";
    }

    printf("你是%s，%s，第%d位入學，可能使用'%s'方式入學\n",
           education_level,
           year_of_student_in_school(student_num[1] - '0', student_num[2] - '0', year),
           num(student_num[3] - '0', student_num[4] - '0', student_num[5] - '0', student_num[6] - '0'),
           type(student_num[3] - '0'));

    // 行銷策略
    int day_of_week = get_day_of_week();
    int last_digit = student_num[7] - '0';

    if ((day_of_week == 1 || day_of_week == 3 || day_of_week == 5 || day_of_week == 0) && (last_digit % 2 != 0)) {
        printf("星期一、三、五、日且學號尾數為奇數：享有特別折扣！\n");
    } else if ((day_of_week == 2 || day_of_week == 4 || day_of_week == 6) && (last_digit % 2 == 0)) {
        printf("星期二、四、六且學號尾數為偶數：享有特別折扣！\n");
    }

    if (contains_digit(student_num, '9')) {
        printf("學號內含有數字 9：享有額外折扣！獲得 任何物品免費折價券 X1\n");
    }

    if (toupper(student_num[0]) == 'D') {
        printf("大學部專屬優惠：獲得 87折 折價券！\n");
    } else if (toupper(student_num[0]) == 'E') {
        printf("進修部優惠：獲得 69折 折價券！\n");
    } else if (toupper(student_num[0]) == 'M') {
        printf("碩士優惠：獲得 49折 折價券！\n");
    } else if (toupper(student_num[0]) == 'P') {
        printf("博士優惠：獲得 1折 折價券！\n");
    }
}

int main() {
    char student_number[10];
    int encode[6] = {8, 7, 6, 8, 7, 6}, multiply_number[100];

    while (printf("請輸入學號 : ") && scanf("%s", student_number) != EOF) {
        int sum = 0, check_number = -1, input_check_number = student_number[7] - '0';
        for (int i = 1; i < 7; i++) {
            multiply_number[i] = (student_number[i] - '0') * encode[i - 1];//把學號2~7位分別成876876
            multiply_number[i] = getnum(multiply_number[i]);//把乘完的結果位數相加 ex:123 = 1 + 2 + 3
            sum += multiply_number[i];  //計算總和 EX 1 + 2 + 3
        }

        check_number = 10 - sum % 10;
        if (check_number == 10) {   //檢查碼為10，讓他=0
            check_number = 0;
        }

        if (input_check_number == check_number) {
            printf("你的學號為真實學號，檢查碼 %d = %d\n", check_number, input_check_number);
            student_number_analyze(student_number, YEAR);
        } else {
            printf("你的學號非真實學號，檢查碼 %d != %d\n", check_number, input_check_number);
            printf("不可以發放折價券\n");
        }
    }
    return 0;
}
