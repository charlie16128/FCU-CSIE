#include <stdio.h>
#include <string.h>

int main(){
    int tc;
    scanf("%d", &tc);
    getchar(); // 清除多餘換行
    while(tc--){
        int press_count[10] = {0}, cpress[10] = {0};
        int c[10] = {0,1,1,1,0,0,1,1,1,1};
        int d[10] = {0,1,1,1,0,0,1,1,1,0};
        int e[10] = {0,1,1,1,0,0,1,1,0,0};
        int f[10] = {0,1,1,1,0,0,1,0,0,0};
        int g[10] = {0,1,1,1,0,0,0,0,0,0};
        int a[10] = {0,1,1,0,0,0,0,0,0,0};
        int b[10] = {0,1,0,0,0,0,0,0,0,0};
        int C[10] = {0,0,1,0,0,0,0,0,0,0};
        int D[10] = {1,1,1,1,0,0,1,1,1,0};
        int E[10] = {1,1,1,1,0,0,1,1,0,0};
        int F[10] = {1,1,1,1,0,0,1,0,0,0};
        int G[10] = {1,1,1,1,0,0,0,0,0,0};
        int A[10] = {1,1,1,0,0,0,0,0,0,0};
        int B[10] = {1,1,0,0,0,0,0,0,0,0};
        
        char t[1005];
        fgets(t, sizeof(t), stdin);
        t[strcspn(t, "\n")] = '\0'; 

        for(int i = 0; t[i] != '\0'; i++){
            int *ptr = NULL;
            switch(t[i]){
                case 'c': ptr = c; break;
                case 'd': ptr = d; break;
                case 'e': ptr = e; break;
                case 'f': ptr = f; break;
                case 'g': ptr = g; break;
                case 'a': ptr = a; break;
                case 'b': ptr = b; break;
                case 'C': ptr = C; break;
                case 'D': ptr = D; break;
                case 'E': ptr = E; break;
                case 'F': ptr = F; break;
                case 'G': ptr = G; break;
                case 'A': ptr = A; break;
                case 'B': ptr = B; break;
            }
            for(int j = 0; j < 10; j++){
                if(ptr[j] && !cpress[j]){
                    press_count[j]++;
                }
                cpress[j] = ptr[j];
            }
        }
      
		// output
        for(int i = 0; i < 10; i++){
            printf("%d", press_count[i]);
            if(i < 9) printf(" ");
        }
        printf("\n");
    }
    return 0;
}
