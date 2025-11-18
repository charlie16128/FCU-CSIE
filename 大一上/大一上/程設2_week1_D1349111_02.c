#include <stdio.h>
#include <stdlib.h>

int get_Quadrant(int x, int y) {
    if (x > 0 && y > 0) return 1;
    if (x < 0 && y > 0) return 2;
    if (x < 0 && y < 0) return 3;
    if (x > 0 && y < 0) return 4;
}

int if_switch(int x1, int y1, int x2, int y2) {
    int dist1 = abs(x1) + abs(y1); 
    int dist2 = abs(x2) + abs(y2);

    if (dist1 != dist2) 
        return dist1 > dist2;

    if (abs(x1) != abs(x2)) 
        return abs(x1) > abs(x2);

    if (abs(y1) != abs(y2)) 
        return abs(y1) > abs(y2);

    return get_Quadrant(x1, y1) > get_Quadrant(x2, y2);
}

int main() {
    int num, range_a, range_b;
    int coord[10000][2];

    scanf("%d %d %d", &num, &range_a, &range_b);
    for (int i = 0; i < num; i++) {
        scanf("%d %d", &coord[i][0], &coord[i][1]);
    }

    for (int i = 0; i < num - 1; i++) {
        for (int j = 0; j < num - 1 - i; j++) {
            if (if_switch(coord[j][0], coord[j][1], coord[j + 1][0], coord[j + 1][1])) {
                int temp_x = coord[j][0], temp_y = coord[j][1];
                coord[j][0] = coord[j + 1][0];
                coord[j][1] = coord[j + 1][1];
                coord[j + 1][0] = temp_x;
                coord[j + 1][1] = temp_y;
            }
        }
    }

    int counter = 0;
    for (int i = 0; i < num; i++) {
        int dist = abs(coord[i][0]) + abs(coord[i][1]);
        if (dist >= range_a && dist <= range_b) {
            counter++;
        }
    }

    printf("%d\n", counter);
    return 0;
}
