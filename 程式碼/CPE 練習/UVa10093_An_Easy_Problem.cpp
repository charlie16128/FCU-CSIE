//An Easy Problem!
#include <bits/stdc++.h>
using namespace std;
int main()
{
    string s;
    while(cin >> s)
    {   
        int k  =0, sum = 0, max = 1,N;
        for(int i = 0; i < s.length();i++)
        {
            if('0' <= s[i] && s[i] <= '9') {
                k = s[i] - '0';
            }
            if('A'<=s[i]&&s[i]<='Z') {
                k = s[i] - 'A' + 10;
            }
            if('a'<=s[i]&&s[i]<='z') {
                k = s[i] - 'a' + 36;
            }
            
            sum += k;
            if(k > max)
                max = k;
        }
        
        for(N = max + 1; N <= 62; N++)
        {
            if(sum % (N - 1) == 0) break;
        }
        if(N <= 62) 
            cout << N << endl;
        else 
            cout<<"such number is impossible!"<<endl;
    }
    return 0;
}
