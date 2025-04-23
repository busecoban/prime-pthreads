#!/usr/bin/env python3
"""

Reads a results file with lines like:
  Threads: 1, Time taken: 124.19 seconds
Computes speed-up and efficiency, then prints a nicely rounded table
and saves an identical PNG with the same formatting.
"""
import sys, re
import matplotlib.pyplot as plt
import pandas as pd

def parse_results(path):
    pattern = re.compile(r'Threads:\s*(\d+),\s*Time taken:\s*([\d\.]+)\s*seconds')
    data = []
    with open(path) as f:
        for line in f:
            m = pattern.search(line)
            if m:
                n = int(m.group(1))
                t = float(m.group(2))
                data.append((n, t))
    return pd.DataFrame(data, columns=['Threads','Time_s'])

def compute_metrics(df):
    t1 = df.loc[df.Threads==1, 'Time_s'].iloc[0]
    df['Speedup']    = t1 / df['Time_s']
    df['Efficiency'] = df['Speedup'] / df['Threads'] * 100
    return df

def format_df(df):
    # Create a new DataFrame of strings with consistent rounding
    df_fmt = pd.DataFrame({
        'Threads'      : df['Threads'].astype(str),
        'Time (s)'     : df['Time_s'].map("{:.2f}".format),
        'Speed-up'     : df['Speedup'].map("{:.2f}".format),
        'Efficiency (%)': df['Efficiency'].map("{:.1f}".format)
    })
    return df_fmt

def print_table(df_fmt):
    # Print Markdown or simple console table
    print(df_fmt.to_markdown(index=False))

def save_table_png(df_fmt, out='metrics_table.png'):
    # Plot the string table
    cell_text = df_fmt.values.tolist()
    col_labels = df_fmt.columns.tolist()

    fig, ax = plt.subplots(figsize=(6, len(df_fmt)*0.4 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=cell_text,
                   colLabels=col_labels,
                   cellLoc='center',
                   loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.2)

    plt.tight_layout()
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Saved table image to {out}")

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: python3 visualize_metrics.py <Results_file>")
        sys.exit(1)

    df = parse_results(sys.argv[1])
    df = compute_metrics(df)
    df_fmt = format_df(df)
    print_table(df_fmt)
    save_table_png(df_fmt)
