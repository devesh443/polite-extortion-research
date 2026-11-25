"""Word counts used in Section IV and Fig. 6; writes word_counts.json.
Usage: python3 word_counts.py /path/to/ransomware_notes
Counts are plain pattern matches, ignoring capitals. Two figures in the paper add a
reading of context: "team" is counted for the writers only in 9 of the 11 notes
(AuditTeam and Kairos use it for the victim's staff), and "criminal" is never used
of the writers."""
import json, re, sys
from notes import sample
GROUPS = {
    "you / your / yours": r"\b(you|your|yours)\b",
    "we / our / us": r"\b(we|our|us)\b",
    "will / won't": r"\b(will|won'?t)\b",
    "if": r"\bif\b",
    "do not / don't": r"\b(do not|don'?t|dont)\b",
    "pay (all forms)": r"\b(pay|pays|paying|payment|payments|paid)\b",
    "please": r"\bplease\b",
    "ransom": r"\bransom\b",
    "thank": r"\bthank\b",
    "sorry / apologise": r"\b(sorry|apologi[sz]e)\b",
    "stole / stolen": r"\b(stole|stolen)\b",
    "downloaded / exfiltrated / copied": r"\b(downloaded|exfiltrated|copied)\b",
    "victim": r"\bvictims?\b",
    "criminal": r"\bcriminals?\b",
    "team": r"\bteams?\b",
}
S = sample(sys.argv[1])
out = {}
print(f"{'word group':36s} occurrences  notes")
for name, pat in GROUPS.items():
    counts = [len(re.findall(pat, text, re.I)) for *_, text in S]
    out[name] = {"occurrences": sum(counts), "notes": sum(c > 0 for c in counts)}
    print(f"{name:36s} {sum(counts):11d}  {out[name]['notes']:5d}")
json.dump(out, open("word_counts.json", "w"), indent=1)
