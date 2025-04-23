prime-pthreadsCSE440 Parallel Programming – Spring 2025
Midterm Project: Multithreaded Prime Number Detection
Student : Buse Çoban — 20200808070
Repo    : github.com/busecoban/prime-pthreads

Build
-----
make            # produces ./primemt



Run
---
./primemt <threads>        (threads = 1 2 4 … 2048)

or 

./run.sh




Description
-----------
The program splits the 1–500 000 000 range into equal sub-ranges,
spawns N POSIX threads, each thread counts primes in its own chunk
using simple trial division, and the main thread prints wall-clock
time measured with gettimeofday(). No shared data structures other
than the final summation (after join), so it is race-free.





Timing results are provided in Results_20200808070.txt.


Initial Timing Results (Trial-Division)
------------------------------------------------------------
Threads: 1, Time taken: 122.439451 seconds
Threads: 2, Time taken: 79.733729 seconds
Threads: 4, Time taken: 46.584816 seconds
Threads: 8, Time taken: 28.431099 seconds
Threads: 16, Time taken: 24.728423 seconds
Threads: 32, Time taken: 24.455278 seconds
Threads: 64, Time taken: 24.164755 seconds
Threads: 128, Time taken: 24.086705 seconds
Threads: 256, Time taken: 24.086165 seconds
Threads: 512, Time taken: 24.088249 seconds
Threads: 1024, Time taken: 24.177125 seconds
Threads: 2048, Time taken: 24.079865 seconds


- Physical Core Limit (8 vCPUs):
Scaling is near-linear only up to the number of available virtual CPUs. Beyond 8 threads, additional threads contend for the same cores, adding only context-switch overhead without meaningful speed-up.

- CPU-Bound Nature of Trial Division:
Every candidate n invokes a √n division loop, making the algorithm heavily compute-bound. While parallelism distributes these loops across cores, each division sequence itself remains strictly serial.

- Amdahl’s Law & Serial Regions:
Fixed serial tasks—thread creation/joining, timing measurements, and result aggregation—occupy a constant portion of total runtime. As a result, theoretical speed-up is capped well below the ideal 8×.

- Cache & Memory Bandwidth Constraints: 
Concurrent threads repeatedly read shared data (e.g. the small-primes list), leading to L3 cache contention and memory-bandwidth thrashing. As thread count increases, this memory traffic approaches hardware limits.

- Thread-Management Overhead:
Launching and scheduling large numbers of threads incurs OS overhead for stack allocation and context switching. When work chunks are small, this overhead can dominate compute time, eroding any incremental gains.


Test1
--------------------------------------------
(venv) busecoban@busesvm:~/prime-pthreads-1$ make
make: 'primemt' is up to date.
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 1
Threads: 1, Time taken: 122.231752 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 2
Threads: 2, Time taken: 78.997726 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 4
Threads: 4, Time taken: 45.900848 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 8
Threads: 8, Time taken: 27.695832 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 16
Threads: 16, Time taken: 24.892340 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 32
Threads: 32, Time taken: 24.713523 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 64
Threads: 64, Time taken: 25.020370 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 128
Threads: 128, Time taken: 24.913054 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 256
Threads: 256, Time taken: 24.961565 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 512
Threads: 512, Time taken: 24.107916 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 1024
Threads: 1024, Time taken: 24.328368 seconds
(venv) busecoban@busesvm:~/prime-pthreads-1$ ./primemt 2048
Threads: 2048, Time taken: 24.426025 seconds


Test2
--------------------------------------------

(venv) busecoban@busesvm:~/prime-pthreads-1$ ./run.sh
Threads: 1, Time taken: 128.439954 seconds
Threads: 2, Time taken: 81.153724 seconds
Threads: 4, Time taken: 45.782009 seconds
Threads: 8, Time taken: 28.463038 seconds
Threads: 16, Time taken: 25.356585 seconds
Threads: 32, Time taken: 24.889127 seconds
Threads: 64, Time taken: 24.845600 seconds
Threads: 128, Time taken: 24.331159 seconds
Threads: 256, Time taken: 24.349084 seconds
Threads: 512, Time taken: 24.218081 seconds
Threads: 1024, Time taken: 24.434173 seconds
Threads: 2048, Time taken: 24.637451 seconds



Segmented-Sieve Timing Results
------------------------------
Threads   Time (s)
-------   -------
1         1.08
2         0.56
4         0.29
8         0.17
16        0.19
32        0.17
64        0.18
128       0.17
256       0.18
512       0.17
1024      0.18
2048      0.18






Segmented-Sieve 
------------------------------------------------------------

Threads: 1, Time taken: 1.08 seconds
Threads: 2, Time taken: 0.56 seconds
Threads: 4, Time taken: 0.29 seconds
Threads: 8, Time taken: 0.17 seconds
Threads: 16, Time taken: 0.19 seconds
Threads: 32, Time taken: 0.17 seconds
Threads: 64, Time taken: 0.18 seconds
Threads: 128, Time taken: 0.17 seconds
Threads: 256, Time taken: 0.18 seconds
Threads: 512, Time taken: 0.17 seconds
Threads: 1024, Time taken: 0.18 seconds
Threads: 2048, Time taken: 0.18 seconds



Trial-Division vs Segmented-Sieve Comparison
--------------------------------------------
• Segmented-Sieve is ~100× faster at 1 thread and ~168× faster at 8 threads.  
• Both plateau beyond 8 threads due to vCPU oversubscription and memory bandwidth limits.
