#!/usr/bin/env python3
import sys, re, csv
import matplotlib.pyplot as plt

# --- 1) Girdi dosyasını komut satırından oku ---
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <results_file>")
    sys.exit(1)
fname = sys.argv[1]

# --- 2) Parse için regex’ler ---
p_thread = re.compile(r"Thread\s+\d+\s+found\s+(\d+)\s+primes")
p_end    = re.compile(r"Threads:\s*(\d+),\s*Time taken:\s*([\d.]+)\s*seconds")

totals = {}   # nthreads → toplam asal sayısı
times  = {}   # nthreads → geçen süre

with open(fname) as f:
    counts = []
    for line in f:
        m = p_thread.search(line)
        if m:
            counts.append(int(m.group(1)))
        else:
            m2 = p_end.search(line)
            if m2:
                n = int(m2.group(1))
                t = float(m2.group(2))
                totals[n] = sum(counts)
                times[n]  = t
                counts = []

# --- 3) Hazır veriler ---
TRUE_TOTAL = 26355867
threads    = sorted(totals)
computed   = [totals[n] for n in threads]
elapsed    = [times[n] for n in threads]
errors     = [computed[i] - TRUE_TOTAL for i in range(len(threads))]

# --- 4) CSV olarak kaydet ---
csv_fname = "prime_count_results.csv"
with open(csv_fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Threads", "Time", "Computed", "True", "Error"])
    for i,n in enumerate(threads):
        writer.writerow([n, f"{elapsed[i]:.6f}", computed[i], TRUE_TOTAL, errors[i]])
print(f"Saved CSV: {csv_fname}")

# --- 5) Grafik 1: Hesaplanan vs Gerçek ---
plt.figure(figsize=(8,5))
plt.plot(threads, computed, 'o-', label="Calculated total")
plt.axhline(TRUE_TOTAL, color='r', linestyle='--', label="True total")
plt.xscale('log', base=2)
plt.xlabel("Threads")
plt.ylabel("Prime count")
plt.title("Calculated vs True Prime Count")
plt.legend()
plt.grid(True, which='both', linestyle=':')
plt.tight_layout()
plt.savefig("prime_count_correctness.png")

# --- 6) Grafik 2: Hata ---
plt.figure(figsize=(8,4))
plt.plot(threads, errors, 's-', color='m')
plt.xscale('log', base=2)
plt.xlabel("Threads")
plt.ylabel("Error (calc − true)")
plt.title("Prime Count Error by Thread Count")
plt.grid(True, which='both', linestyle=':')
plt.tight_layout()
plt.savefig("prime_count_error.png")

# --- 7) Tablo olarak da PNG üret ---
from matplotlib.table import Table

fig, ax = plt.subplots(figsize=(10, 0.5 + len(threads)*0.25))
ax.axis('off')
tbl = Table(ax, bbox=[0,0,1,1])

# sütun başlıkları
cols = ["Threads", "Time", "Computed", "True", "Error"]
cell_w = 1.0 / len(cols)
cell_h = 1.0 / (len(threads) + 1)

# header
for j, header in enumerate(cols):
    tbl.add_cell(0, j, cell_w, cell_h, text=header, loc='center', facecolor="#cccccc")

# veri satırları
for i, n in enumerate(threads, start=1):
    row = [n, f"{elapsed[i-1]:.6f}", computed[i-1], TRUE_TOTAL, errors[i-1]]
    for j, val in enumerate(row):
        tbl.add_cell(i, j, cell_w, cell_h, text=str(val), loc='center')

ax.add_table(tbl)
plt.savefig("prime_count_table.png")

print("Saved images: prime_count_correctness.png, prime_count_error.png, prime_count_table.png")
