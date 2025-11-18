#include <stdio.h>

int main(){
    int tc;
    scanf("%d",&tc);
    while(tc--){
        int num;
        scanf("%d",&num);

        char ch;
        int value, list[256] = {0};
        for(int i = 0; i < num; i++){
            scanf(" %c %d",&ch, &value); // 注意%c前要有空白去除\n
            list[(int)ch] = value;
        }

        long long total = 0;
        int line_num;
        char line[10005];
        scanf("%d",&line_num);
        getchar();

        for(int i = 0; i < line_num; i++){
            fgets(line, 10000, stdin);
            for(int k = 0; line[k] != '\0'; k++){
                total += list[line[k]];
            }
        }
        
        printf("%d.%02d$\n", (int)(total / 100), (int)(total % 100));
    }
    return 0;
}


// #include <stdio.h>

// int main(){
//     int tc;
//     scanf("%d",&tc);
//     while(tc--){
//         int num;
//         scanf("%d",&num);

//         int value, list[256] = {0};
//         char ch;
//         for(int i = 0; i < num; i++){
//             scanf(" %c %d",&ch, &value);
//             list[(int)ch] = value;
//         }

//         int total = 0;
//         int line;
//         char input[10005];
//         scanf("%d",&line);
//         getchar();

//         for(int i = 0; i < line; i++){
//             fgets(input, 10000, stdin);
//             for(int k = 0; input[k] != '\0'; k++){
//                 total += list[input[k]];
//             }
//         }

//         printf("%d.%02d$\n", total / 100, total % 100);
        
//     }
//     return 0;
// }

#include <stdio.h>

int main(){
    int tc;
    scanf("%d",&tc);
    while(tc--){
        int num;
        scanf("%d",&num);

        char ch;
        int value, map[265] = {0};
        for(int i = 0; i < num; i++){
            scanf(" %c %d",&ch, &value);
            map[(int)ch] = value;
        }

        int line, total = 0;
        char input[10005];
        scanf("%d",&line);
        getchar();

        for(int i = 0; i < line; i++){
            fgets(input, 10000, stdin);
            for(int k = 0; input[k] != '\0'; k++){
                total += map[input[k]];
            }
        }

        printf("%d.%02d$\n", total / 100, total % 100);

    }
    return 0;
}