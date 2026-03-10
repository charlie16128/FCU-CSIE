#include <bits/stdc++.h>

using namespace std;

int algorithm(long long n){
    int count = 1;
    while(n != 1){
        if(n % 2 != 0){
            n = 3 * n + 1;
        }else{
            n = n / 2;
        }
        count++;
    }
    return count;
}

int main(){
    int i, j;
    while(cin >> i >> j){
        cout << i << " " << j << " ";

        if(i > j) swap(i ,j);

        int Max_Cycle_length = 0;

        for(int k = i; k < j; k++){
            int current_cycle_length = algorithm(k);
            //Max_Cycle_length = (current_cycle_length > Max_Cycle_length) ? current_cycle_length : Max_Cycle_length;
            Max_Cycle_length = max(Max_Cycle_length, current_cycle_length);
        }
        cout << Max_Cycle_length << endl;
    }
    return 0;
}

//https://zerojudge.tw/ShowProblem?problemid=c039
