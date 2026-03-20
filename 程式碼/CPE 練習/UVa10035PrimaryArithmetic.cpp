#include <bits/stdc++.h>
using namespace std;    

int main(){
    int first, second;
    while(cin >> first >> second && (first != 0 && second != 0)){
        int carry = 0, count = 0;
        while(a || b){
            if(a % 10 + b % 10 + carry >= 10){
                count++;
                carry = 1;
            }else{
                carry = 0;
            }
        }
        
        if(count == 0){
            cout << "No carry operation." << endl;
        }else{
            cout << count << " carry operation." << endl;
        }
    }

    return 0;
}
