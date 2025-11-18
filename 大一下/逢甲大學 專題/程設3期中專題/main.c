#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <Windows.h>
#include <conio.h>
#include <time.h>

#define ROAD_LENGTH 80
#define DINO_PLACE 6

typedef struct {
    char road[ROAD_LENGTH + 1];
    int jump_Time_Left;
    int score;
    int wait_Time;
    int barrier_Chance;
    int hp;
    time_t start_time;
    int longjump_chance;
    bool has_power;
    int power_left;
    bool power_mode;
    int start_animation;
} Dino;

// 初始化
Dino* init() {
    Dino* MyDinoPtr = (Dino*)malloc(sizeof(Dino));
    if (MyDinoPtr != NULL) {
        MyDinoPtr->barrier_Chance = 10;
        MyDinoPtr->jump_Time_Left = 0;
        MyDinoPtr->score = 0;
        MyDinoPtr->wait_Time = 150;
        MyDinoPtr->hp = 3;
        MyDinoPtr->start_time = time(NULL);
        MyDinoPtr->longjump_chance = 5;
        MyDinoPtr->has_power = false;
        MyDinoPtr->power_left = 0;
        MyDinoPtr->power_mode = false;
        MyDinoPtr->start_animation = 0;
        for (int i = 0; i < ROAD_LENGTH; i++) {
            MyDinoPtr->road[i] = '_';
        }
        MyDinoPtr->road[ROAD_LENGTH] = '\0';
    }
    return MyDinoPtr;
}

// 顯示畫面
void display(Dino* MyDinoPtr) {
    system("cls");
    time_t now = time(NULL);
    int elapsed = (int)(now - MyDinoPtr->start_time);
    printf("Time: %02d:%02d", elapsed / 60, elapsed % 60);

    printf("\tHP: ");
    for (int i = 0; i < MyDinoPtr->hp; i++) {
        printf("@ ");
    }

    if (MyDinoPtr->has_power) {
        printf("\tShield(G)");
    }

    // 空中
    printf("\n\n\t");
    for (int i = 0; i < ROAD_LENGTH; i++) {
        if (i == DINO_PLACE && MyDinoPtr->jump_Time_Left > 0) {
            printf(MyDinoPtr->power_mode ? "O" : "o");
        }
        else {
            printf(" ");
        }
    }

    // 地面
    printf("\n\t");
    for (int i = 0; i < ROAD_LENGTH; i++) {
        if (i == DINO_PLACE && MyDinoPtr->jump_Time_Left == 0) {
            printf(MyDinoPtr->power_mode ? "O" : "o");
        }
        else {
            printf("%c", MyDinoPtr->road[i]);
        }
        // 啟動動畫
        if (MyDinoPtr->start_animation == 0) Sleep(30); 
    }
    
    printf("\n\n\n\t\tYour score is: %d\n", MyDinoPtr->score);
    MyDinoPtr->start_animation = 1;
}

// 移動
void move(Dino* MyDinoPtr) {
    for (int i = 0; i < ROAD_LENGTH; i++) {
        MyDinoPtr->road[i] = MyDinoPtr->road[i + 1];
    }
    MyDinoPtr->road[ROAD_LENGTH - 1] = '_';
}

// 按鍵
bool space_pressed() {
    return _kbhit() && _getch() == 32;
}
bool g_pressed() {
    return _kbhit() && _getch() == 'g';
}

// 撞到障礙物
bool is_bumped(Dino* MyDinoPtr) {
    return MyDinoPtr->jump_Time_Left == 0 && MyDinoPtr->road[DINO_PLACE] == 'X';
}

// 撞到道具
bool is_on_item(Dino* MyDinoPtr) {
    return MyDinoPtr->road[DINO_PLACE] == '*';
}

// 隨機障礙物
bool spawn_barrier(Dino* MyDinoPtr) {
    return rand() % 100 < MyDinoPtr->barrier_Chance;
}

// 隨機道具
bool spawn_item(Dino* MyDinoPtr) {
    return rand() % 100 < MyDinoPtr->longjump_chance;
}

// 死亡動畫
void death_animation(Dino* MyDinoPtr) {
    time_t end_time = time(NULL);
    int total_seconds = (int)(end_time - MyDinoPtr->start_time);
    Sleep(1000);
    system("cls");
    printf("\n\n\n\t\tGame \tOver! \n");
    printf("\t\tYour score was: %d \n", MyDinoPtr->score);
    printf("\t\tTotal Time %02d:%02d\n\n", total_seconds / 60, total_seconds % 60);
}

// 主程式
int main() {
    srand(time(NULL));
    Dino* MyDinoPtr = init();
    display(MyDinoPtr);

    while (true) {
        time_t now = time(NULL);
        int elapsed = (int)(now - MyDinoPtr->start_time);
        
        // 時間倍率設定
        float speed_multiplier = 1.0f + (elapsed / 15) * 0.25f;
        if (speed_multiplier > 3.0f) {
            speed_multiplier = 3.0f;
        }
        int sleep_time = (int)(MyDinoPtr->wait_Time / speed_multiplier);

        // 使用護頓道具
        if (_kbhit()) {
            int key = _getch();
            if (key == 32 && MyDinoPtr->jump_Time_Left == 0) {
                MyDinoPtr->jump_Time_Left = 7;
            }
            else if (key == 'g' && MyDinoPtr->has_power && !MyDinoPtr->power_mode) {
                MyDinoPtr->power_mode = true;
            }
        }

        // debug
        //if (_kbhit()) {
        //    char ch = _getch();
        //    if (ch == 32 && MyDinoPtr->jump_Time_Left == 0) { // 空白鍵跳躍
        //        MyDinoPtr->jump_Time_Left = 7;
        //    }
        //    else if (ch == 'P' || ch == 'p') { // 外掛加血
        //        if (MyDinoPtr->hp) {
        //            MyDinoPtr->hp++;
        //        }
        //    }
        //    else if (ch == 'G' || ch == 'g') {
        //        // 如果你也有加無敵功能，就放在這裡
        //    }
        //}

        if (MyDinoPtr->power_mode) {
            MyDinoPtr->power_left--;
            if (MyDinoPtr->power_left <= 0) {
                MyDinoPtr->power_mode = false;
                MyDinoPtr->has_power = false;
            }
        }

        move(MyDinoPtr);

        if (MyDinoPtr->jump_Time_Left > 0) {
            MyDinoPtr->jump_Time_Left--;
        }

        if (spawn_barrier(MyDinoPtr)) {
            MyDinoPtr->road[ROAD_LENGTH - 1] = 'X';
        }
        else if (spawn_item(MyDinoPtr)) {
            MyDinoPtr->road[ROAD_LENGTH - 1] = '*';
        }

        if (is_on_item(MyDinoPtr)) {
            MyDinoPtr->has_power = true;
            MyDinoPtr->power_left = 10;
            MyDinoPtr->road[DINO_PLACE] = '_';
        }

        if (is_bumped(MyDinoPtr)) {
            if (!MyDinoPtr->power_mode) {
                MyDinoPtr->hp--;
                if (MyDinoPtr->hp == 0) {
                    display(MyDinoPtr);
                    death_animation(MyDinoPtr);
                    break;
                }
            }
        }

        display(MyDinoPtr);
        MyDinoPtr->score++;
        Sleep(sleep_time);
    }

    free(MyDinoPtr);
    return 0;
}