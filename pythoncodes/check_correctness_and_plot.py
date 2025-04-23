#!/usr/bin/env python3
"""

For each thread count:
  - run './primetest <threads>' 
  - parse both “Total primes found:” and “Threads: N, Time taken: X seconds”
Verify that all prime counts agree, then plot Time vs Threads.
"""
import re, subprocess, sys
import matplotlib.pyplot as plt

# Test edilecek thread listesi
THREADS = [1,2,4,8,16,32,64,128,256,512,1024,2048]

# Regex kalıpları
re_time   = re.compile(r"Threads:\s*\d+,\s*Time taken:\s*([\d\.]+)\s*seconds")
re_primes = re.compile(r"Total primes found:\s*(\d+)")

times = {}
counts = {}

# Her thread için primetest'i çalıştır
for t in THREADS:
    out = subprocess.check_output(["./primetest", str(t)], text=True)
    # Zamanı al
    m_time = re_time.search(out)
    if not m_time:
        print(f"❌ Zamanı ayrıştırırken hata ({t} threads)") 
        sys.exit(1)
    times[t] = float(m_time.group(1))
    # Prime sayısını al
    m_pr  = re_primes.search(out)
    if not m_pr:
        print(f"❌ Prime sayısını ayrıştırırken hata ({t} threads)")
        sys.exit(1)
    counts[t] = int(m_pr.group(1))
    print(f"Threads={t:<4} Time={times[t]:>6.2f}s  Primes={counts[t]}")

# Doğruluk kontrolü: hepsi aynı sayıyı bulmuş mu?
unique_counts = set(counts.values())
if len(unique_counts) == 1:
    total = unique_counts.pop()
    print(f"\n✅ Correct! All runs found {total} primes.")
else:
    print("\n⚠️ Mismatch in prime counts:", counts)
    sys.exit(1)

# Grafik çizimi
threads = list(times.keys())
time_vals = [times[t] for t in threads]

plt.figure(figsize=(8,5))
plt.plot(threads, time_vals, 'o-', color='tab:blue', label='Time (s)')
plt.xscale('log', base=2)
plt.xlabel('Number of Threads')
plt.ylabel('Time (seconds)')
plt.title(f'Prime Counting Performance ({total} primes)')
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('primetest_performance.png', dpi=300)
plt.show()
