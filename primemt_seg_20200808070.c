/* primemt_seg_20200808070.c – Segmented Sieve + Pthreads */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <sys/time.h>
#include <stdint.h>   // uintptr_t için

#define MAX 500000000UL
#define SEG 1000000UL  /* 1M’lik segment */

typedef struct { unsigned long low, high; } task_t;

unsigned long *base_primes;
int base_count;

void precompute() {
    unsigned long limit = sqrt(MAX);
    char *mark = calloc(limit+1,1);
    base_primes = malloc((limit/2)*sizeof *base_primes);
    for (unsigned long p=2; p<=limit; ++p) {
        if (!mark[p]) {
            base_primes[base_count++] = p;
            for (unsigned long i=p*p; i<=limit; i+=p) mark[i]=1;
        }
    }
    free(mark);
}

void *worker(void *arg) {
    task_t *t = arg;
    unsigned long count = 0;
    char *segment = calloc(SEG,1);
    for (unsigned long low = t->low; low < t->high; low += SEG) {
        unsigned long high = low + SEG;
        if (high > t->high) high = t->high;
        memset(segment,0,high-low);
        for (int i=0; i<base_count; ++i) {
            unsigned long p = base_primes[i];
            unsigned long start = (low + p - 1)/p * p;
            for (unsigned long j=start; j<high; j+=p)
                segment[j-low] = 1;
        }
        if (low == 0) segment[0]=segment[1]=1;
        for (unsigned long i=low; i<high; ++i)
            if (!segment[i-low]) ++count;
    }
    free(segment);
    return (void*)(uintptr_t)count;
}

int main(int ac,char **av) {
    if (ac!=2) { fprintf(stderr,"usage: %s <threads>\n",av[0]); return 1; }
    int n = atoi(av[1]);
    precompute();
    pthread_t *th = malloc(n * sizeof *th);
    task_t *tk = malloc(n * sizeof *tk);
    unsigned long range = MAX / n;
    struct timeval s,e; gettimeofday(&s,0);
    for (int i=0; i<n; ++i) {
        tk[i].low  = i*range;
        tk[i].high = (i==n-1 ? MAX : (i+1)*range);
        pthread_create(&th[i], NULL, worker, &tk[i]);
    }
    unsigned long total = 0;
    for (int i=0; i<n; ++i) {
        void *ret;
        pthread_join(th[i], &ret);
        total += (unsigned long)(uintptr_t)ret;
    }
    gettimeofday(&e,0);
    double sec = (e.tv_sec - s.tv_sec) + (e.tv_usec - s.tv_usec)/1e6;
    printf("Threads: %d, Time taken: %.6f seconds\n", n, sec);
    return 0;
}
