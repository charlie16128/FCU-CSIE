#include <bits/stdc++>
using namespace std;

void com(int i, int j){
    if(i > j){
        int temp = i;
        i = j;
        j = temp;
    }
}

int algorithm(int n){
    if(n == 1) return 1;

    if(n % 2 != 0){
        n = 3*n + 1;
        return n;
    }else{}
        n = n / 2;
        return n;
}

int main(){
    int i, j;
    while(cin >> i >> j){
        com(i,j);
        int CL = 0;
        vector<int> list;
        for(;i <= j; i++){
            list.pushback(algorithm(i));
        }
    }

    return 0;
}

//https://zerojudge.tw/ShowProblem?problemid=c039
