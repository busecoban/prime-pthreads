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


## İlk Ölçüm Sonuçları (trial-division)
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


## İlk Zaman Ölçümleri (Trial-Division)

| Thread | Süre (s) |
| :----: | :------: |
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

* **Fiziksel çekirdek sınırı** aşılınca (M3 Pro’da 8 P + 4 E) çekirdekler paylaşılmaya başlanıyor; bağlam değiştirme (context-switch) ek yük getiriyor.  
* **Hafıza-bağımlı** algoritma: her iş parçacığı aynı büyük asal test döngüsünü yapıyor, önbellek faydası sınırlı; bellek bant genişliği darboğaz oluyor.  
* İş başına yük küçüldükçe (64 thread → 7.8 M sayı) planlama maliyeti kazanımdan fazla hâle geliyor.

> Sonraki adım olarak segmented sieve uygulanacak; iyileşme olmazsa bu plateau raporda tartışılacaktır.



