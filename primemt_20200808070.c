/*  primemt_20200808070.c
    CSE440 — Spring 2025 Midterm
    Multithreaded prime counter for the range [1, 500,000,000]

    Compile : make
    Run     : ./primemt <threads>
    Output  : Threads: N, Time taken: X.XXXXXX seconds
*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <sys/time.h>

#define MAX 500000000UL  /* inclusive upper bound for prime search */

/* 
 * Structure to hold the range each thread will process
 * and the count of primes found in that range.
 */
typedef struct {
    uint64_t start;  /* inclusive start of range */
    uint64_t end;    /* exclusive end of range */
    uint64_t count;  /* number of primes found */
} range_t;

/*
 * Simple trial-division primality test.
 * Returns 1 if n is prime, 0 otherwise.
 */
static int is_prime(uint64_t n) {
    if (n < 2)                 return 0;  /* 0 and 1 are not prime */
    if (n == 2)                return 1;  /* 2 is prime */
    if (n % 2 == 0)            return 0;  /* even numbers >2 are not prime */

    /* only test odd divisors up to sqrt(n) */
    uint64_t limit = (uint64_t) sqrt((double) n);
    for (uint64_t i = 3; i <= limit; i += 2) {
        if (n % i == 0)        return 0;  /* divisible => not prime */
    }
    return 1;  /* no divisor found => prime */
}

/*
 * Worker function for each thread.
 * Loops through its assigned subrange and increments count
 * for each prime found.
 */
static void *worker(void *arg) {
    range_t *rng = (range_t *)arg;
    for (uint64_t i = rng->start; i < rng->end; ++i) {
        rng->count += is_prime(i);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    /* Check for correct usage */
    if (argc != 2) {
        fprintf(stderr, "usage: %s <num_threads>\n", argv[0]);
        return EXIT_FAILURE;
    }

    /* Parse thread count and validate */
    int nthreads = atoi(argv[1]);
    if (nthreads < 1) {
        fprintf(stderr, "num_threads must be positive\n");
        return EXIT_FAILURE;
    }

    /* Allocate arrays for thread IDs and their range data */
    pthread_t *tid = malloc(nthreads * sizeof *tid);
    range_t   *seg = malloc(nthreads * sizeof *seg);
    if (!tid || !seg) {
        perror("malloc");
        return EXIT_FAILURE;
    }

    /* Compute the size of each chunk (subrange) */
    uint64_t chunk = MAX / nthreads;

    /* Start the timer */
    struct timeval t0, t1;
    gettimeofday(&t0, NULL);

    /* Launch threads */
    for (int i = 0; i < nthreads; ++i) {
        /* Determine this thread's start (inclusive) and end (exclusive) */
        seg[i].start = (uint64_t)i * chunk + 1;
        seg[i].end   = (i == nthreads - 1)
                       ? (MAX + 1)                  /* last thread goes to MAX */
                       : ((uint64_t)(i + 1) * chunk + 1);
        seg[i].count = 0;

        /* Initialize thread attributes (e.g., custom stack size) */
        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setstacksize(&attr, 256 * 1024);  /* 256 KB stack */

        /* Create the thread, passing its range struct as argument */
        if (pthread_create(&tid[i], &attr, worker, &seg[i]) != 0) {
            perror("pthread_create");
            return EXIT_FAILURE;
        }

        pthread_attr_destroy(&attr);
    }

    /* Wait for all threads to finish and accumulate results */
    uint64_t total_primes = 0;
    for (int i = 0; i < nthreads; ++i) {
        pthread_join(tid[i], NULL);
        total_primes += seg[i].count;
    }

    /* Stop the timer */
    gettimeofday(&t1, NULL);
    double elapsed = (t1.tv_sec - t0.tv_sec)
                   + (t1.tv_usec - t0.tv_usec) / 1e6;

    /* Print the performance result */
    printf("Threads: %d, Time taken: %.6f seconds\n", nthreads, elapsed);

    /* Clean up and exit */
    free(tid);
    free(seg);
    return EXIT_SUCCESS;
}
