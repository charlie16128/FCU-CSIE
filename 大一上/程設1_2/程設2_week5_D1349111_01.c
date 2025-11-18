#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char line1[101], line2[101];
    while (scanf("%s %s",line1,line2) != EOF) {
        int freq1[26] = {0}, freq2[26] = {0};
        for(int i=0; line1[i]; i++)
            freq1[line1[i] - 'A']++;
        for(int i=0; line2[i]; i++)
            freq2[line2[i] - 'A']++;
        
        qsort(freq1, 26, sizeof(int), (int(*)(const void*, const void*))strcmp);
        qsort(freq2, 26, sizeof(int), (int(*)(const void*, const void*))strcmp);

        int same = 1;
        for(int i=0; i<26; i++){
            if(freq1[i] != freq2[i]){
                same = 0;
                break;
            }
        }
        printf(same ? "YES\n" : "NO\n");
    }
    return 0;
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       