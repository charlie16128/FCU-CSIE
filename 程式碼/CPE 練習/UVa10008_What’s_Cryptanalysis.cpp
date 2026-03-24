#include <bits/stdc++.h>
using namespace std;

int main(){
    int tc, table[26] = {0}, max = 0;
    cin >> tc;
    cin.ignore();

    while(tc--){
        string s;
        getline(cin, s);

        for(int i = 0; i < s.length(); i++){
            if(isalpha(s[i])){
                int index = toupper(s[i]) - 'A';
                table[index]++;
                if(table[index] > max){
                    max = table[index];
                }
            }
        }
    }
    
    for(int i = max; i >= 1; i--){
        for(int k = 0; k < 26; k++){
            if(table[k] == i){
                cout << char(k + 'A') << " " << i << endl;
            }
        }
    }
    return 0;
}