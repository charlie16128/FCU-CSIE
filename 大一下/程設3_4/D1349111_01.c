#include <stdio.h>

int main(){
    FILE *fin_ptr, *fout_ptr;
    fin_ptr = fopen("input.txt", "r");
    fout_ptr = fopen("output.txt", "w");

    if(fin_ptr != NULL && fout_ptr != NULL){
        int word;
        while((word = fgetc(fin_ptr)) != EOF){
            fputc(word, fout_ptr);
        }
    }

    fclose(fin_ptr);
    fclose(fout_ptr);
    return 0;
}