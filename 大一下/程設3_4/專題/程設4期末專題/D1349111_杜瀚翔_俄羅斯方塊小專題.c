#define _CRT_SECURE_NO_WARNINGS // 禁用安全性警告

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <windows.h>


#define CANVAS_WIDTH 10
#define CANVAS_HEIGHT 20

#define FALL_DELAY 500
#define RENDER_DELAY 100

// 鍵盤對照表
#define LEFT_KEY 0x25
#define RIGHT_KEY 0x27 
#define ROTATE_KEY 0x26 
#define DOWN_KEY 0x28 
#define FALL_KEY 0x20 
#define HOLD_KEY 0x43 // 新增：C 鍵

// 判斷按鍵是否有被按下的函式
#define LEFT_FUNC() GetAsyncKeyState(LEFT_KEY) & 0x8000
#define RIGHT_FUNC() GetAsyncKeyState(RIGHT_KEY) & 0x8000
#define ROTATE_FUNC() GetAsyncKeyState(ROTATE_KEY) & 0x8000
#define DOWN_FUNC() GetAsyncKeyState(DOWN_KEY) & 0x8000
#define FALL_FUNC() GetAsyncKeyState(FALL_KEY) & 0x8000
#define HOLD_FUNC() (GetAsyncKeyState(HOLD_KEY) & 0x8000) // 新增

int highscores[5] = { 0 }; // 新增：紀錄前五名
FILE* fp = NULL;

typedef enum
{
    RED = 41,
    GREEN,
    YELLOW,
    BLUE,
    PURPLE,
    CYAN,
    WHITE,
    BLACK = 0,
} Color;

typedef enum
{
    EMPTY = -1,
    I,
    J,
    L,
    O,
    S,
    T,
    Z
} ShapeId;

typedef struct
{
    ShapeId shape;
    Color color;
    int size;
    char rotates[4][4][4];
} Shape;

typedef struct
{
    int x;
    int y;
    int score;
    int rotate;
    int fallTime;
    ShapeId queue[4];
    ShapeId hold; // 新增：暫存的方塊
    bool holdUsed; // 新增：本回合是否使用過 Hold
} State;

typedef struct
{
    Color color;
    ShapeId shape;
    bool current;
} Block;

Shape shapes[7] = {
    {.shape = I,
     .color = CYAN,
     .size = 4,
     .rotates =
         {
             {{0, 0, 0, 0},
              {1, 1, 1, 1},
              {0, 0, 0, 0},
              {0, 0, 0, 0}},
             {{0, 0, 1, 0},
              {0, 0, 1, 0},
              {0, 0, 1, 0},
              {0, 0, 1, 0}},
             {{0, 0, 0, 0},
              {0, 0, 0, 0},
              {1, 1, 1, 1},
              {0, 0, 0, 0}},
             {{0, 1, 0, 0},
              {0, 1, 0, 0},
              {0, 1, 0, 0},
              {0, 1, 0, 0}}}},
    {.shape = J,
     .color = BLUE,
     .size = 3,
     .rotates =
         {
             {{1, 0, 0},
              {1, 1, 1},
              {0, 0, 0}},
             {{0, 1, 1},
              {0, 1, 0},
              {0, 1, 0}},
             {{0, 0, 0},
              {1, 1, 1},
              {0, 0, 1}},
             {{0, 1, 0},
              {0, 1, 0},
              {1, 1, 0}}}},
    {.shape = L,
     .color = YELLOW,
     .size = 3,
     .rotates =
         {
             {{0, 0, 1},
              {1, 1, 1},
              {0, 0, 0}},
             {{0, 1, 0},
              {0, 1, 0},
              {0, 1, 1}},
             {{0, 0, 0},
              {1, 1, 1},
              {1, 0, 0}},
             {{1, 1, 0},
              {0, 1, 0},
              {0, 1, 0}}}},
    {.shape = O,
     .color = WHITE,
     .size = 2,
     .rotates =
         {
             {{1, 1},
              {1, 1}},
             {{1, 1},
              {1, 1}},
             {{1, 1},
              {1, 1}},
             {{1, 1},
              {1, 1}}}},
    {.shape = S,
     .color = GREEN,
     .size = 3,
     .rotates =
         {
             {{0, 1, 1},
              {1, 1, 0},
              {0, 0, 0}},
             {{0, 1, 0},
              {0, 1, 1},
              {0, 0, 1}},
             {{0, 0, 0},
              {0, 1, 1},
              {1, 1, 0}},
             {{1, 0, 0},
              {1, 1, 0},
              {0, 1, 0}}}},
    {.shape = T,
     .color = PURPLE,
     .size = 3,
     .rotates =
         {
             {{0, 1, 0},
              {1, 1, 1},
              {0, 0, 0}},

             {{0, 1, 0},
              {0, 1, 1},
              {0, 1, 0}},
             {{0, 0, 0},
              {1, 1, 1},
              {0, 1, 0}},
             {{0, 1, 0},
              {1, 1, 0},
              {0, 1, 0}}}},
    {.shape = Z,
     .color = RED,
     .size = 3,
     .rotates =
         {
             {{1, 1, 0},
              {0, 1, 1},
              {0, 0, 0}},
             {{0, 0, 1},
              {0, 1, 1},
              {0, 1, 0}},
             {{0, 0, 0},
              {1, 1, 0},
              {0, 1, 1}},
             {{0, 1, 0},
              {1, 1, 0},
              {1, 0, 0}}}},
};

void setBlock(Block* block, Color color, ShapeId shape, bool current)
{
    block->color = color;
    block->shape = shape;
    block->current = current;
}

void resetBlock(Block* block)
{
    block->color = BLACK;
    block->shape = EMPTY;
    block->current = false;
}

void printCanvas(Block canvas[CANVAS_HEIGHT][CANVAS_WIDTH], State* state)
{
    printf("\033[0;0H\n");
    for (int i = 0; i < CANVAS_HEIGHT; i++)
    {
        printf("|");
        for (int j = 0; j < CANVAS_WIDTH; j++)
        {
            printf("\033[%dm\u3000", canvas[i][j].color);
        }
        printf("\033[0m|\n");
    }

    // 輸出Next:
    printf("\033[%d;%dHNext:", 3, CANVAS_WIDTH * 2 + 5);
    // 新增：顯示 Hold
    printf("\033[%d;%dHHold:", 3, CANVAS_WIDTH * 2 + 30);
    if (state->hold != EMPTY) {
        Shape holdShape = shapes[state->hold];
        for (int j = 0; j < 4; j++) {
            printf("\033[%d;%dH", 4 + j, CANVAS_WIDTH * 2 + 35);
            for (int k = 0; k < 4; k++) {
                if (j < holdShape.size && k < holdShape.size && holdShape.rotates[0][j][k]) {
                    printf("\x1b[%dm  ", holdShape.color);
                }
                else {
                    printf("\x1b[0m  ");
                }
            }
        }
    }

    // 新增：顯示分數
    printf("\033[%d;%dHScore: %d", 17, CANVAS_WIDTH * 2 + 5, state->score);

    // 輸出有甚麼方塊
    for (int i = 1; i <= 3; i++)
    {
        Shape shapeData = shapes[state->queue[i]];
        for (int j = 0; j < 4; j++)
        {
            printf("\033[%d;%dH", i * 4 + j, CANVAS_WIDTH * 2 + 15);
            for (int k = 0; k < 4; k++)
            {
                if (j < shapeData.size && k < shapeData.size && shapeData.rotates[0][j][k])
                {
                    printf("\x1b[%dm  ", shapeData.color);
                }
                else
                {
                    printf("\x1b[0m  ");
                }
            }
        }
    }
    return;
}

bool move(Block canvas[CANVAS_HEIGHT][CANVAS_WIDTH], int originalX, int originalY, int originalRotate, int newX, int newY, int newRotate, ShapeId shapeId)
{
    Shape shapeData = shapes[shapeId];
    int size = shapeData.size;

    // 判斷方塊有沒有不符合條件
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            if (shapeData.rotates[newRotate][i][j])
            {
                // 判斷有沒有出去邊界
                if (newX + j < 0 || newX + j >= CANVAS_WIDTH || newY + i < 0 || newY + i >= CANVAS_HEIGHT)
                {
                    return false;
                }
                // 判斷有沒有碰到別的方塊
                if (!canvas[newY + i][newX + j].current && canvas[newY + i][newX + j].shape != EMPTY)
                {
                    return false;
                }
            }
        }
    }

    // 移除方塊舊的位置
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            if (shapeData.rotates[originalRotate][i][j])
            {
                resetBlock(&canvas[originalY + i][originalX + j]);
            }
        }
    }

    // 移動方塊至新的位置
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            if (shapeData.rotates[newRotate][i][j])
            {
                setBlock(&canvas[newY + i][newX + j], shapeData.color, shapeId, true);
            }
        }
    }

    return true;
}

int clearLine(Block canvas[CANVAS_HEIGHT][CANVAS_WIDTH])
{
    for (int i = 0; i < CANVAS_HEIGHT; i++)
    {
        for (int j = 0; j < CANVAS_WIDTH; j++)
        {
            if (canvas[i][j].current)
            {
                canvas[i][j].current = false;
            }
        }
    }

    int linesCleared = 0;
    for (int i = CANVAS_HEIGHT - 1; i >= 0; i--)
    {
        bool isFull = true;
        for (int j = 0; j < CANVAS_WIDTH; j++)
        {
            if (canvas[i][j].shape == EMPTY) {
                isFull = false;
                break;
            }
        }
        if (isFull) {
            linesCleared += 1;

            for (int j = i; j > 0; j--)
            {
                for (int k = 0; k < CANVAS_WIDTH; k++)
                {
                    setBlock(&canvas[j][k], canvas[j - 1][k].color, canvas[j - 1][k].shape, false);
                    resetBlock(&canvas[j - 1][k]);
                }
            }
            i++;
        }
    }
    return linesCleared;
}


void logic(Block canvas[CANVAS_HEIGHT][CANVAS_WIDTH], State* state)
{
    if (ROTATE_FUNC())
    {
        int newRotate = (state->rotate + 1) % 4;
        if (move(canvas, state->x, state->y, state->rotate, state->x, state->y, newRotate, state->queue[0]))
        {
            state->rotate = newRotate;
        }
    }
    else if (LEFT_FUNC())
    {
        if (move(canvas, state->x, state->y, state->rotate, state->x - 1, state->y, state->rotate, state->queue[0]))
        {
            state->x -= 1;
        }
    }
    else if (RIGHT_FUNC())
    {
        if (move(canvas, state->x, state->y, state->rotate, state->x + 1, state->y, state->rotate, state->queue[0]))
        {
            state->x += 1;
        }
    }
    else if (DOWN_FUNC())
    {
        state->fallTime = FALL_DELAY;
    }
    else if (FALL_FUNC())
    {
        state->fallTime += FALL_DELAY * CANVAS_HEIGHT;
    }
    // 新增：Hold 方塊
    else if (HOLD_FUNC() && !state->holdUsed) {
        ShapeId temp = state->hold;
        state->hold = state->queue[0];
        state->holdUsed = true;

        // 移除目前方塊
        Shape shapeData = shapes[state->queue[0]];
        for (int i = 0; i < shapeData.size; i++) {
            for (int j = 0; j < shapeData.size; j++) {
                if (shapeData.rotates[state->rotate][i][j]) {
                    resetBlock(&canvas[state->y + i][state->x + j]);
                }
            }
        }

        // 換成 hold 裡的方塊（若沒東西就用 queue[1]）
        if (temp == EMPTY) {
            state->queue[0] = state->queue[1];
            state->queue[1] = state->queue[2];
            state->queue[2] = state->queue[3];
            state->queue[3] = rand() % 7;
            state->holdUsed = false; // 新增：新方塊產生後重置 Hold 使用狀態

        }
        else {
            state->queue[0] = temp;
        }

        state->x = CANVAS_WIDTH / 2;
        state->y = 0;
        state->rotate = 0;

        move(canvas, state->x, state->y, 0, state->x, state->y, 0, state->queue[0]);
    }


    state->fallTime += RENDER_DELAY;

    while (state->fallTime >= FALL_DELAY)
    {
        state->fallTime -= FALL_DELAY;
        if (move(canvas, state->x, state->y, state->rotate, state->x, state->y + 1, state->rotate, state->queue[0]))
        {
            state->y++;
        }
        else
        {
            state->score += clearLine(canvas);

            state->x = CANVAS_WIDTH / 2;
            state->y = 0;
            state->rotate = 0;
            state->fallTime = 0;
            state->queue[0] = state->queue[1];
            state->queue[1] = state->queue[2];
            state->queue[2] = state->queue[3];
            state->queue[3] = rand() % 7;

            //結束輸出
            if (!move(canvas, state->x, state->y, state->rotate, state->x, state->y, state->rotate, state->queue[0]))
            {
                printf("\033[%d;%dH\x1b[41m GAME OVER \x1b[0m\033[%d;%dH", CANVAS_HEIGHT - 3, CANVAS_WIDTH * 2 + 5, CANVAS_HEIGHT + 5, 0);
                // 新增：更新排行榜
                for (int i = 0; i < 5; i++) {
                    if (state->score > highscores[i]) {
                        for (int j = 4; j > i; j--) {
                            highscores[j] = highscores[j - 1];
                        }
                        highscores[i] = state->score;
                        break;
                    }
                }
                fp = fopen("highscore.txt", "w");
                if (fp) {
                    for (int i = 0; i < 5; i++) {
                        fprintf(fp, "%d\n", highscores[i]);
                    }
                    fclose(fp);
                }

                // 新增：顯示排行榜
                printf("\033[%d;%dHHigh Scores:", CANVAS_HEIGHT + 2, 0);
                for (int i = 0; i < 5; i++) {
                    printf("\033[%d;%dH%2d. %d", CANVAS_HEIGHT + 3 + i, 2, i + 1, highscores[i]);
                }
                
                Sleep(1000);


                // 動畫 2：清空整個畫面（canvas 區域）
                for (int row = 0; row < CANVAS_HEIGHT; row++) {
                    for (int col = 0; col < CANVAS_WIDTH; col++) {
                        resetBlock(&canvas[row][col]);
                    }
                    Sleep(20);
                }
                printCanvas(canvas, state);
                Sleep(200);

                // 清除畫面右側 UI 區域
                int speed = 200;
                for (int row = 0; row < CANVAS_HEIGHT + 10; row++) {
                    printf("\033[%d;%dH\033[0m", row + 1, 0);
                    for (int i = 0; i < 100; i++) {
                        printf(" ");
                    }
                    if (speed - 20) speed -= 20;
                    Sleep(speed);
                }

                // 新增：顯示學號動畫
                const char* id = "D1349111";
                int id_len = 8;
                int id_colors[8] = { 41, 43, 42, 44, 45, 43, 43, 43 }; // ANSI 背景色碼（紅、橙、橙、綠、藍、紫、紅、橙）

                int startX = 2;
     
                for (int i = 0; i < id_len; i++) {
                    printf("\033[%d;%dH\033[%dm %c \033[0m", 5, startX + i * 3, id_colors[i], id[i]); // 每個字 3 格寬
                    Sleep(200); // 每個字延遲
                }


                exit(0);//結束遊戲
            }
        }
    }
    return;
}

int main()
{
    srand((unsigned int)time(NULL)); // 明確轉型，編譯器不會再警告

    State state = {
        .x = CANVAS_WIDTH / 2,
        .y = 0,
        .score = 0,
        .rotate = 0,
        .fallTime = 0 
    };

    state.hold = EMPTY; // 新增
    state.holdUsed = false; // 新增

    fopen_s(&fp, "highscore.txt", "r"); // 新增
    if (fp) {
        for (int i = 0; i < 5; i++) {
            fscanf(fp, "%d", &highscores[i]);

        }
        fclose(fp);
    }

    for (int i = 0; i < 4; i++)
    {
        state.queue[i] = rand() % 7;
    }

    Block canvas[CANVAS_HEIGHT][CANVAS_WIDTH];
    for (int i = 0; i < CANVAS_HEIGHT; i++)
    {
        for (int j = 0; j < CANVAS_WIDTH; j++)
        {
            resetBlock(&canvas[i][j]);
        }
    }

    Shape shapeData = shapes[state.queue[0]];

    for (int i = 0; i < shapeData.size; i++)
    {
        for (int j = 0; j < shapeData.size; j++)
        {
            if (shapeData.rotates[0][i][j])
            {
                setBlock(&canvas[state.y + i][state.x + j], shapeData.color, state.queue[0], true);
            }
        }
    }

    while (1)
    {
        printCanvas(canvas, &state);
        logic(canvas, &state);
        Sleep(100);
    }

    return 0;
}
