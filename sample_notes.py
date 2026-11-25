"""List the sample and write sample_stats.json.
Usage: python3 sample_notes.py /path/to/ransomware_notes"""
import json, os, sys
from notes import read, n_words, sample
root = sys.argv[1]
S = sample(root, verbose=True)
folders = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")]
no_txt = sum(1 for d in folders if not any(f.lower().endswith(".txt") for f in os.listdir(os.path.join(root, d))))
stats = {"folders": len(folders), "no_txt": no_txt, "with_txt": len(folders) - no_txt,
         "sample": len(S), "words": sum(x[2] for x in S)}
stats["eligible"] = sum(1 for d in folders
                        for t in [sorted((f for f in os.listdir(os.path.join(root, d)) if f.lower().endswith(".txt")), key=str.lower)]
                        if t and n_words(read(os.path.join(root, d, t[0]))) >= 100)
stats["short"] = stats["with_txt"] - stats["eligible"]
json.dump(stats, open("sample_stats.json", "w"), indent=1)
for i, (d, f, n, _) in enumerate(S, 1):
    print(i, d, f, n, sep="\t")
