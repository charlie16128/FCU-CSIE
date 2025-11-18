// #include <stdio.h>

// int main(){
//     long long n, rev, temp, count;
//     int t;
//     scanf("%d", &t);
//     while(t--){
//         scanf("%lld",&n);
//         count = 0;
//         while(1){
//             rev = 0;
//             temp = n;
//             while(temp){
//                 rev = rev * 10 + temp % 10;
//                 temp /= 10;
//             }
            
//             if(rev == n && count != 0){
//                 printf("%lld %lld\n",count, n);
//                 break;
//             }

//             n += rev;
//             count++;
//         }
//     }   
//     return 0;
// }





// #include <stdio.h>

// int main(){
//     long long input, count, rev, temp;
//     int t;
//     scanf("%d",&t);
    
//     while(t--){
//         scanf("%lld",&input);
//         count = 0;
//         while(1){
//             rev = 0;
//             temp = input;
//             while(temp){
//                 rev = rev * 10 +  temp % 10;
//                 temp /= 10;
//             }

//             if(rev == input && count != 0){
//                 printf("%lld %lld\n",count, input);
//                 break;
//             }
//             count++;
//             input += rev;
//         }
//     }
//     return 0;
// }

// #include <stdio.h>
// #include <string.h>

// int main(){
//     long long input, rev, temp, counter;
//     int tc;
//     scanf("%d",&tc);
//     while(tc--){
//         scanf("%lld",&input);
//         counter = 0;
//         while(1){
//             rev = 0;
//             temp = input;
//             while(temp){
//                 rev = rev * 10 + temp % 10;
//                 temp /= 10;
//             }
//             if(rev == input && counter != 0){
//                 printf("%lld %lld\n",counter, input);
//                 break;
//             }
//             counter++;
//             input += rev;
//         }
//     }
//     return 0;
// }

#include <stdio.h>
#include <string.h>

int main(){
    long long input, rev, temp, counter;
    int tc;
    scanf("%d",&tc);
    while(tc--){
        scanf("%lld",&input);
        counter = 0;
        while(1){
            temp = input;
            rev = 0;
            while(temp){
                rev = rev * 10 + temp % 10;
                temp /= 10;
            }

            if(rev == input && counter != 0){
                printf("%lld %lld\n",counter, input);
                break;
            }
            counter++;
            input += rev;
        }
    }
    return 0;
}