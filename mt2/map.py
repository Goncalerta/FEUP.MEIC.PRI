import json

queries = ["q1", "q2", "q3", "q4"]
systems = ["sys1", "sys2", "sys1_syn", "sys2_syn"]

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

sum_values = {k: v / total_ap[k] for k, v in total_sum.items()}
json.dump(sum_values, open("map.json", "w"))
