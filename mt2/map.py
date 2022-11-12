import os

queries = ["q1", "q2"]
systems = ["sys1", "sys2", "sys3"]

total_sum = {k: 0 for k in systems}
total_ap = {k: 0 for k in systems}
for query in queries:
    for system in systems:
        try:
            with open(f"{query}/{system}/ap.txt", "r") as f:
                lines = f.readlines()
                total_sum[system] += float(lines[0].strip())
                total_ap[system] += 1
        except FileNotFoundError:
            pass

print({k: v / total_ap[k] for k, v in total_sum.items()})
