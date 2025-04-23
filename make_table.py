#!/usr/bin/env python3
"""

Reads a results file with lines like:
  Threads: 1, Time taken: 122.439451 seconds
and creates a PNG image of the table.
"""
import sys
import re
import matplotlib.pyplot as plt

def parse_results(path):
    pattern = re.compile(r'Threads:\s*(\d+),\s*Time taken:\s*([\d\.]+)\s*seconds')
    data = []
    with open(path) as f:
        for line in f:
            m = pattern.search(line)
            if m:
                data.append((m.group(1), m.group(2)))
    return data

def make_table_image(data, out_png='results_table.png'):
    # Prepare table data
    col_labels = ["Threads", "Time (s)"]
    table_data = data

    # Create figure
    fig, ax = plt.subplots(figsize=(4, len(data)*0.4 + 1))
    ax.axis('off')
    ax.axis('tight')

    # Create table
    tbl = ax.table(cellText=table_data, colLabels=col_labels, loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.5)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    print(f'Table image saved to {out_png}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 make_table_png.py <results_file>")
        sys.exit(1)
    data = parse_results(sys.argv[1])
    if not data:
        print("No valid lines found in the results file.")
        sys.exit(1)
    make_table_image(data)
