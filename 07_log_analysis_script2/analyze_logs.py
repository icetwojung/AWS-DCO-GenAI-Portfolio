import glob
import os

log_dir = os.path.dirname(os.path.abspath(__file__))
log_files = sorted(glob.glob(os.path.join(log_dir, "server*.log")))

keywords = ["CRC error", "Link Down"]

print(f"{'서버':<15} {'CRC error':>12} {'Link Down':>12}")
print("-" * 42)

totals = {kw: 0 for kw in keywords}

for log_file in log_files:
    server_name = os.path.basename(log_file)
    counts = {kw: 0 for kw in keywords}

    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for kw in keywords:
                if kw in line:
                    counts[kw] += 1

    for kw in keywords:
        totals[kw] += counts[kw]

    print(f"{server_name:<15} {counts['CRC error']:>12} {counts['Link Down']:>12}")

print("-" * 42)
print(f"{'합계':<15} {totals['CRC error']:>12} {totals['Link Down']:>12}")
