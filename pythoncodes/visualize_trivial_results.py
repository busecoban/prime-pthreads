#!/usr/bin/env python3
"""
visualize_trivial_results.py

Reads a Results file from trial-division runs and plots:
  - Time vs Threads
  - Speed-up vs Threads

Usage:
  python3 visualize_trivial_results.py Results_20200808070.txt
"""
import sys
import re
import matplotlib.pyplot as plt

def parse_results(path):
    threads = []
    times = []
    pattern = re.compile(r'Threads:\s*(\d+),\s*Time taken:\s*([\d\.]+)\s*seconds')
    with open(path) as f:
        for line in f:
            m = pattern.search(line)
            if m:
                threads.append(int(m.group(1)))
                times.append(float(m.group(2)))
    return threads, times

def plot_results(threads, times, out_png='trivial_performance.png'):
    # compute speed-up relative to single-thread
    base_time = times[0]
    speedup = [base_time / t for t in times]

    fig, ax1 = plt.subplots(figsize=(8,5))
    ax1.plot(threads, times, 'o-', color='tab:blue', label='Time (s)')
    ax1.set_xscale('log', base=2)
    ax1.set_xlabel('Number of Threads')
    ax1.set_ylabel('Time (seconds)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True, which='both', linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(threads, speedup, 's--', color='tab:red', label='Speed-up')
    ax2.set_ylabel('Speed-up', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='best')

    plt.title('Trial-Division Prime Counting Performance')
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    print(f'Plot saved to {out_png}')
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 visualize_trivial_results.py <Results_file>")
        sys.exit(1)
    threads, times = parse_results(sys.argv[1])
    plot_results(threads, times)
