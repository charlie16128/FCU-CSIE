#include <stdio.h>

int main(){
    FILE *fin_ptr, *fout_ptr;

    fin_ptr = fopen("input.txt", "r");
    fout_ptr = fopen("output.txt", "w");

    int n;
    fscanf(fin_ptr, "%d", &n);

    int a[105] = {0};
    for(int i = 0; i < n; i++){
        fscanf(fin_ptr, "%d", &a[i]);
    }

    int num;
    fscanf(fin_ptr, "%d", &num);

    for(int i = 0; i < n - 1; i++){
        for(int j = 0; j < n - i - 1; j++){
            if(a[j] > a[j + 1]){
                int temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
    
    int find = -1;
    for(int i = 0; i < n; i++){
        fprintf(fout_ptr, "%d", a[i]);
        if(i != n - 1){
            fprintf(fout_ptr, " ");
        }
        if(a[i] == num){
            find = i;
        }
    }
    fprintf(fout_ptr, "\n");
    fprintf(fout_ptr, "%d\n", find);

    fclose(fin_ptr);
    fclose(fout_ptr);
    // printf("DONE");
    return 0;
}