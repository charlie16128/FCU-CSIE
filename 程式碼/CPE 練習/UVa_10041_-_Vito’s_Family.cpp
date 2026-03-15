#include <bits/stdc++.h>
using namespace std;

int main(){
    int tc;
    cin >> tc;

    while(tc--){
        int r;
        cin >> r;
        
        vector<int> s(r);
        for(auto &x : s){
            cin >> x;
        }

        sort(s.begin(), s.end());

        int mid = s[r / 2];

        long long res = 0;
        for(int x : s){
            res += abs(mid - x);
        }

        cout << res << "\n";
    }
    return 0;
}