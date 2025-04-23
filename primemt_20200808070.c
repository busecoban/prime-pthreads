/*  primemt_20200808070.c
    CSE440 — Spring 2025 Midterm
    Multithreaded prime counter for the range [1, 500 000 000]

    Compile :  make
    Run      :  ./primemt <threads>
    Output   :  Threads: N, Time taken: X.XXXXXX seconds
*/
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <sys/time.h>

#define MAX 500000000UL          /* inclusive upper bound */

/* her thread’in çalışacağı aralık ve bulduğu asal adedi */
typedef struct {
    uint64_t start, end;         /* [start, end)  yarı-açık aralık */
    uint64_t count;
} range_t;

/* basit deneme-bölme (trial division) -> küçük aralıklarda yeterli */
static int is_prime(uint64_t n)
{
    if (n < 2)               return 0;
    if (n == 2)              return 1;
    if (n % 2 == 0)          return 0;
    uint64_t r = (uint64_t) sqrt((double) n);
    for (uint64_t i = 3; i <= r; i += 2)
        if (n % i == 0)      return 0;
    return 1;
}

/* pthread giriş fonksiyonu */
static void *worker(void *arg)
{
    range_t *rng = arg;
    for (uint64_t i = rng->start; i < rng->end; ++i)
        rng->count += is_prime(i);
    return NULL;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s <num_threads>\n", argv[0]);
        return 1;
    }
    int nthreads = atoi(argv[1]);
    if (nthreads < 1) {
        fprintf(stderr, "num_threads must be positive\n");
        return 1;
    }

    /* --- diziler oluştur --- */
    pthread_t *tid  = malloc(nthreads * sizeof *tid);
    range_t   *seg  = malloc(nthreads * sizeof *seg);
    if (!tid || !seg) { perror("malloc"); return 1; }

    uint64_t chunk = MAX / nthreads;          /* eşit bölme */

    /* --- kronometre başlat --- */
    struct timeval t0, t1;
    gettimeofday(&t0, NULL);

    /* --- thread’leri başlat --- */
    for (int i = 0; i < nthreads; ++i) {
        seg[i].start = i * chunk + 1;
        seg[i].end   = (i == nthreads - 1) ? MAX + 1 : (i + 1) * chunk + 1;
        seg[i].count = 0;

        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setstacksize(&attr, 256 * 1024);   /* 256 KB stack */
        if (pthread_create(&tid[i], &attr, worker, &seg[i]) != 0) {
            perror("pthread_create"); return 1;
        }
        pthread_attr_destroy(&attr);
    }

    /* --- thread’leri bitir ve toplamla --- */
    uint64_t total = 0;
    for (int i = 0; i < nthreads; ++i) {
        pthread_join(tid[i], NULL);
        total += seg[i].count;
    }

    /* --- kronometre durdur --- */
    gettimeofday(&t1, NULL);
    double sec = (t1.tv_sec - t0.tv_sec) +
                 (t1.tv_usec - t0.tv_usec) / 1e6;

    printf("Threads: %d, Time taken: %.6f seconds\n", nthreads, sec);
    /*  printf("Total primes = %lu\n", total);   // doğruluk kontrolü için */

    free(tid); free(seg);
    return 0;
}
