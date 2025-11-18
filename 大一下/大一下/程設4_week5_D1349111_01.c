#include <stdio.h>

typedef struct{
    int data[100000];
    int front;
    int rear;
}Queue;

void iniQueue(Queue *q){
    q->front = 0;
    q->rear = 0;
}

void enqueue(Queue *q, int value){
    q->data[q->rear++] = value;
}

void dequeue(Queue *q){
    if(q->front < q->rear){
        q->front++;
    }
}

int peek(Queue *q){
    if(q->front < q->rear){
        return q->data[q->front];
    }
    else{
        return -1;
    }
}

int size(Queue *q){
    return q->rear - q->front;
}

int main(){
    int n;
    scanf("%d",&n);

    Queue q;
    iniQueue(&q);

    for(int loop = 0; loop < n; loop++){
        int k, x;
        scanf("%d", &k);
        if(k == 1){
            scanf("%d",&x);
            enqueue(&q, x);
        }else if(k == 2){
            printf("%d\n",peek(&q));
        }else if(k == 3){
            dequeue(&q);
        }else if(k == 4){
            printf("%d\n", size(&q));
        }
    }
    return 0;
}