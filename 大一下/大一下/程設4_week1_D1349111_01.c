#include <stdio.h>
#include <string.h>

int test(char a, char b){
    return (a == 'R' && b == 'S') || (a == 'S' && b == 'P') || (a == 'P' && b == 'R');
}

void simulate(char terr[105][105], char new[105][105], int r, int c){
    int x[] = {-1, 1, 0, 0}; // row 上下左右時 ex: terr[x][y];
    int y[] = {0, 0, -1, 1}; // column 上下左右時
    
    for(int i = 0; i < r; i++){ // 列
        for(int k = 0; k < c; k++){ // 行
            new[i][k] = terr[i][k]; 
            
            for(int dir = 0; dir < 4; dir++){
                int new_i = i + x[dir];
                int new_k = k + y[dir];

                if(new_i >= 0 && new_i < r && new_k >= 0 && new_k < c){
                    if(test(terr[new_i][new_k], terr[i][k])){
                        new[i][k] = terr[new_i][new_k];
                        break;
                    }
                }
            }
        }
    }
}

int main(){
    int tc;
    scanf("%d",&tc);

    while(tc--){
        char terr[105][105], new[105][105]; 
        int r, c, n;
        scanf("%d %d %d",&r, &c, &n);
        for(int i = 0; i < r; i++){
            scanf("%s",terr[i]);
        }
        
        for(int day = 1; day <= n; day++){
            simulate(terr, new, r, c);

            for(int i = 0; i < r; i++){
                for(int k = 0; k < c; k++){
                    terr[i][k] = new[i][k];
                }
            }
        }

        for(int i = 0; i < r; i++){
            printf("%s\n",terr[i]);
        }

        if(tc) printf("\n");
    }
    return 0;
}