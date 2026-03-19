#include <bits/stdc++.h>
using namespace std;

int main(){
    int tc;
    cin >> tc;
    while(tc--){
        int sim_day, pnum, p[105] = {0};
        cin >> sim_day >> pnum;
        for (int i = 0; i < pnum; i++){
            cin >> p[i];
        }

        int table[3655] = {0}, k;
        for (int i = 0; i < pnum; i++){
            k = 1;
            for (int j = p[i]; j <= sim_day; j = p[i] * k){
                if((j % 6 != 0) && (j % 7 != 0))
                    table[j] = 1;
                k++;
            }
        }

        int counter = 0;
        for (int i = 0; i < sim_day; i++){
            if(table[i] == 1){
                counter++;
            }
        }
        cout << counter << endl;
    }

    return 0;
}
