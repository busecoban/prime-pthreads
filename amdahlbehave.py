import matplotlib.pyplot as plt
import numpy as np

# Ölçülen veriler
threads = np.array([1,2,4,8,16,32,64,128,256,512,1024,2048])
times =    np.array([124.19,79.31,45.68,28.51,25.46,24.27,24.13,23.93,24.02,24.11,23.97,24.11])

# Hesaplanan speed-up
speedup_measured = times[0] / times

# Amdahl'ın seri payı S (maks speedup ~1/S)
S = 1.0 / speedup_measured.max()
# Amdahl'ın teorik speed-up'u
speedup_amdahl = 1.0 / (S + (1-S)/threads)

plt.figure(figsize=(8,5))
plt.plot(threads, speedup_measured, 'o-', label='Measured speed-up')
plt.plot(threads, speedup_amdahl, '--', label="Amdahl's Law", color='orange')
plt.xscale('log', base=2)
plt.xlabel('Number of threads')
plt.ylabel('Speed-up')
plt.title("Measured vs Amdahl's Law Speed-up")
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('amdahl_vs_measured.png', dpi=300)
plt.show()
