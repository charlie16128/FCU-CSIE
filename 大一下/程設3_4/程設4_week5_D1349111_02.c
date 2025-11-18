#include <stdio.h>

typedef struct{
    int data[500];
    int front;
    int rear;
}Queue;

void iniQueue(Queue *q){
    q->front = 0;
    q->rear = 0;
}

void push(Queue *q, int val){
    q->data[q->rear++] = val;
}

int pop(Queue *q){
    return q->data[q->front++];
}

int qsize(Queue *q){
    return q->rear - q->front;
}
int main(){
    int n;
    while(scanf("%d",&n) && n){
        Queue q;
        iniQueue(&q);

        for(int i = 1; i <= n; i++){
            push(&q, i);
        }

        printf("Discarded cards:");
        while(qsize(&q) >= 2){
            printf(" %d", pop(&q));
            
            // 還可再做下一次
            if(qsize(&q) >= 2){
                printf(",");
            }

            int top_card = pop(&q);
            push(&q, top_card);
        }
        printf("\nRemaining card: %d\n", pop(&q));
    }
    return 0;
}