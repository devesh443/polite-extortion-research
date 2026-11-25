"""Statistics reported in the paper, from the coding sheet.
Usage: python3 analyse_coding.py"""
import csv, statistics
rows = [r for r in csv.DictReader(open("ransom_notes_coding_sheet.csv")) if r["No."].isdigit()]
items = list(rows[0].keys())[4:26]
I = lambda r, k: int(r[k])
IDX = "Business-writing index (0-5)"
print("Notes with each item (of 45):")
for k in items:
    n = sum(I(r, k) for r in rows); print(f"  {k:42s} {n:2d}  {round(100*n/45)}%")
secs = [sum(I(r, k) for k in items[:11]) for r in rows]
print(f"\nSections per note: mean {sum(secs)/45:.1f}, min {min(secs)}, max {max(secs)}")
for r in rows:  # check the index against its definition
    calc = (I(r, "Service vocabulary") + I(r, "Commercial vocabulary") + I(r, "Business motive or professional identity")
            + max(I(r, "Deletion or confidentiality promise"), I(r, "Security report")) + I(r, "Politeness markers"))
    assert calc == int(r[IDX]), r["Group folder"]
idx = [int(r[IDX]) for r in rows]
print(f"Index: >=3 in {sum(v >= 3 for v in idx)} notes, 5 in {[r['Group folder'] for r in rows if r[IDX] == '5']}, 0 in {idx.count(0)}")
three = ["Service vocabulary", "Commercial vocabulary", "Business motive or professional identity"]
print(f"Any of the three business features: {sum(any(I(r, k) for k in three) for r in rows)}; all three: {sum(all(I(r, k) for k in three) for r in rows)}")
def split(name, cond):
    a = [r for r in rows if cond(r)]; b = [r for r in rows if not cond(r)]
    print(f"Threat | {name}: with {sum(I(r,'Threat') for r in a)}/{len(a)}, without {sum(I(r,'Threat') for r in b)}/{len(b)}")
    return a, b
split("politeness markers", lambda r: I(r, "Politeness markers"))
split("reassurance", lambda r: I(r, "Reassurance"))
hi, lo = split("index >= 3", lambda r: int(r[IDX]) >= 3)
print(f"Median words: index>=3 {statistics.median(int(r['Words']) for r in hi)}, others {statistics.median(int(r['Words']) for r in lo)}")
print(f"Legal consequences: index>=3 {sum(I(r,'Legal consequences') for r in hi)}/{len(hi)}, others {sum(I(r,'Legal consequences') for r in lo)}/{len(lo)}")
w = [int(r["Words"]) for r in rows]
print(f"Words: total {sum(w)}, min {min(w)}, max {max(w)}, median {statistics.median(w)}")
