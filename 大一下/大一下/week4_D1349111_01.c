#include <stdio.h>

int main(){
    int tc;
    scanf("%d",&tc);
    
    while(tc--){
        int day, political, h[1000], ans = 0;
        scanf("%d %d",&day, &political);
        
        for(int i = 0; i < political; i++){
            scanf("%d",&h[i]);
        }

        for(int i = 1; i <= day; i++){
            for(int k = 0; k < political; k++){
                if(i % 7 != 6 && i % 7 != 0 && i % h[k] == 0){
                    ans++;
                    break;
                }
            }
        }

        printf("%d\n",ans);
    }
    return 0;
}