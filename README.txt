# prime-pthreadsCSE440 Parallel Programming – Spring 2025
Midterm Project: Multithreaded Prime Number Detection
Student : Buse Çoban — 20200808070
Repo    : github.com/busecoban/prime-pthreads

Build
-----
make            # produces ./primemt

Run
---
./primemt <threads>        (threads = 1 2 4 … 2048)

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

- **vCPU:** 8  
- **RAM:** 6 GB  
- **Disk:** 40 GB virtio-blk  
- **İşletim Sistemi:** Ubuntu 24.04 LTS  
- **Test Komutları:** `./primemt <threads>` ve `./primemt_seg <threads>`

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

Initial Timing Results (Trial-Division)
------------------------------
Threads   Time (s)
-------   -------
| 1  | 122.44 |
| 2  | 79.73 |
| 4  | 46.58 |
| 8  | 28.43 |
| 16 | 24.73 |
| 32 | 24.46 |
| 64 | 24.16 |
| 128| 24.09 |
| 256| 24.09 |
| 512| 24.09 |
| 1024| 24.18 |
| 2048| 24.08 |

### Neden 16 iş parçacığından sonra ~24 s’de plato?

* **vCPU sınırı (8)**  
  UTM, konuk Ubuntu’ya 8 sanal çekirdek (vCPU) gösteriyor.  
  16 ve üzeri iş parçacığında, her sanal çekirdeği en az iki thread paylaşmak zorunda kalıyor. Bu da
  bağlam değiştirme (context-switch) maliyetini getiriyor.

* **Hypervisor zaman paylaşımlı planlama**  
  QEMU/Apple Virtualization Framework, vCPU’ları gerçek çekirdeklere sırayla
  atıyor. Hazır‐çalıştır döngüsü arttıkça CPU darboğazı oluşuyor; ek thread’ler hız
  kazandırmıyor.

* **Bellek-bağımlı (trial division) algoritma**  
  Her iş parçacığı kendi dizisinde tekil sayıları denediği için önbellek
  paylaşımı sınırlı. Çekirdekler arttıkça bellek bant genişliği ve L2/SLC
  trafiği sabit kalıyor → ek CPU zamanı boşa gidiyor.





Segmented-Sieve 
------------------------------------------------------------

- **vCPU:** 8  
- **RAM:** 6 GB  
- **Disk:** 40 GB virtio-blk  
- **İşletim Sistemi:** Ubuntu 24.04 LTS  
- **Test Komutları:** `./primemt <threads>` ve `./primemt_seg <threads>`

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





Trial-Division vs Segmented-Sieve Comparison
--------------------------------------------
• Segmented-Sieve is ~100× faster at 1 thread and ~168× faster at 8 threads.  
• Both plateau beyond 8 threads due to vCPU oversubscription and memory bandwidth limits.


VM Hardware Change and Rationale
--------------------------------
Observed plateau at ~24 s beyond 8 threads:  
- vCPU limit (8) in VM → oversubscription (multiple threads share each vCPU) → context-switch overhead.  
- Hypervisor scheduling maps vCPUs onto physical cores in timeslices.  

Solution:  
Increased VM vCPU to 12 and RAM to 8 GB.  
Expect continued speedup up to 12 threads; will retest to observe new plateau.



