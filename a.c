#include <stdio.h>
#include <stdlib.h>

long long functioncalc(int A[], int N) {
    long long asd = 0;
    int dsa = abs(A[0]);
    int neg_count = 0;
    
    for (int i = 0; i < N; i++) {
        int abs_val = abs(A[i]);
        asd += abs_val;
        if (abs_val < dsa) {
            dsa = abs_val;
        }
        if (A[i] < 0) {
            neg_count++;
        }
    }
    
    if (neg_count % 2 != 0) {
        asd -= 2 * dsa;
    }
    
    return asd;
}

int main() {
    int Test;
    scanf("%d", &Test);
    while (Test--) {
        int N;
        scanf("%d", &N);
        int arr[N];
        for (int i = 0; i < N; i++) {
            scanf("%d", &arr[i]);
        }
        printf("%lld\n", functioncalc(arr, N));
    }
    return 0;
}