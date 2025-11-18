#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char ch;
    struct Node *next;
} Node;

int main() {
    char input[100005];
    while (scanf("%s", input) != EOF) {
        Node *head = (Node *)malloc(sizeof(Node));
        Node *tail = head;
        head->next = NULL;

        Node *curr = head; // curr是插入的位置（在curr後面插入）

        for (int i = 0; input[i] != '\0'; i++) {
            if (input[i] == '[') {
                curr = head;
            } 
            else if (input[i] == ']') {
                curr = tail;
            } 
            else {
                Node *newNode = (Node *)malloc(sizeof(Node));
                newNode->ch = input[i];
                newNode->next = curr->next;
                curr->next = newNode;
                if (curr == tail) {
                    tail = newNode; // 如果剛好插在尾巴，要更新tail
                }
                curr = newNode; // 插完後curr移到新節點
            }
        }

        // Output
        Node *now = head->next;
        while (now != NULL) {
            printf("%c", now->ch);
            now = now->next;
        }
        printf("\n");

        // Free memory
        now = head;
        while (now != NULL) {
            Node *temp = now;
            now = now->next;
            free(temp);
        }
    }
    return 0;
}
