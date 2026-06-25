#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_CHARS 256

typedef struct Node {
    int freq;
    unsigned char ch;
    struct Node *left, *right;
} Node;

typedef struct {
    Node **data;
    int size, cap;
} MinHeap;

Node *new_node(unsigned char ch, int freq) {
    Node *n = malloc(sizeof(Node));
    n->ch = ch; n->freq = freq;
    n->left = n->right = NULL;
    return n;
}

void heap_push(MinHeap *h, Node *n) {
    h->data[h->size++] = n;
    int i = h->size - 1;
    while (i > 0) {
        int p = (i-1)/2;
        if (h->data[p]->freq <= h->data[i]->freq) break;
        Node *t = h->data[p]; h->data[p] = h->data[i]; h->data[i] = t;
        i = p;
    }
}

Node *heap_pop(MinHeap *h) {
    Node *top = h->data[0];
    h->data[0] = h->data[--h->size];
    int i = 0;
    while (1) {
        int s = i, l = 2*i+1, r = 2*i+2;
        if (l < h->size && h->data[l]->freq < h->data[s]->freq) s = l;
        if (r < h->size && h->data[r]->freq < h->data[s]->freq) s = r;
        if (s == i) break;
        Node *t = h->data[i]; h->data[i] = h->data[s]; h->data[s] = t;
        i = s;
    }
    return top;
}

int code_len[MAX_CHARS];

void build_codes(Node *root, int depth) {
    if (!root) return;
    if (!root->left && !root->right) {
        code_len[root->ch] = depth ? depth : 1;
        return;
    }
    build_codes(root->left,  depth + 1);
    build_codes(root->right, depth + 1);
}

void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

int main() {
    char *text = malloc(1000002);
    scanf("%s", text);
    int len = strlen(text);

    int freq[MAX_CHARS] = {0};
    for (int i = 0; i < len; i++) freq[(unsigned char)text[i]]++;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    MinHeap h;
    h.data = malloc(MAX_CHARS * sizeof(Node*));
    h.size = 0; h.cap = MAX_CHARS;

    int unique = 0;
    for (int i = 0; i < MAX_CHARS; i++)
        if (freq[i]) { heap_push(&h, new_node(i, freq[i])); unique++; }

    while (h.size > 1) {
        Node *l = heap_pop(&h);
        Node *r = heap_pop(&h);
        Node *p = new_node(0, l->freq + r->freq);
        p->left = l; p->right = r;
        heap_push(&h, p);
    }

    Node *root = h.size ? heap_pop(&h) : NULL;
    memset(code_len, 0, sizeof(code_len));
    build_codes(root, 0);

    long long total_bits = 0;
    for (int i = 0; i < MAX_CHARS; i++)
        if (freq[i]) total_bits += (long long)freq[i] * code_len[i];

    clock_gettime(CLOCK_MONOTONIC, &end);
    double ms = (end.tv_sec  - start.tv_sec)  * 1000.0
              + (end.tv_nsec - start.tv_nsec) / 1e6;

    double ratio = (double)total_bits / (8.0 * len);
    printf("%d\n%lld\n%.2f\n", unique, total_bits, ratio);
    fprintf(stderr, "%.3f\n", ms);

    free_tree(root);
    free(h.data);
    free(text);
    return 0;
}