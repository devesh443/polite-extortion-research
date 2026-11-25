"""Position of each section's first cue phrase (Fig. 3, Table V).
Usage: python3 section_order.py /path/to/ransomware_notes   (writes pos.json)"""
import re, json, statistics, sys
from notes import sample
S = sample(sys.argv[1])
CUES={
 'Greeting': r"^\W*(hello|hi\b|dear\b|good (day|morning|afternoon|evening)|greetings|welcome|attn|attention)",
 'Announcement': r"\b(encrypted|breached|compromised|hacked|penetrated|locked|infected|attacked)\b",
 'Data theft claim': r"\b(stole|stolen|downloaded|exfiltrated|copied|leak(ed)?|publish(ed)?)\b",
 'Reassurance': r"(don'?t worry|do not worry|can be (restored|recovered|decrypted|returned)|(is|are) possible|not (lost|damaged)|we can (help|restore|recover|decrypt)|easily|solve)",
 'Proof or guarantee': r"(test decrypt|free decrypt|for free|guarantee|proof|decrypt (one|1|2|3|two|three|several|some) files?)",
 'Contact instructions': r"\b(contact|write to us|email|e-mail|tor browser|onion|chat|qtox|tox id|session|jabber|telegram)\b",
 'Deadline': r"\b\d+\s*(hours?|hrs|days?|h)\b|\b(hours|days)\b",
 'Threat': r"(will be (published|leaked|deleted|destroyed|sold|lost|released|made public)|we will (publish|leak|delete|destroy|sell|release)|permanently|lose|forever|never (be|get|recover)|otherwise)",
 'Technical warnings': r"(do not|don'?t|dont)\s+(try|rename|modify|delete|edit|use|change|restart|shut|reboot|turn off|attempt|move)",
 'Discouraging outside help': r"\b(police|fbi|law enforcement|authorities|recovery (company|companies|firms?|services)|negotiators?|insurance|third.part(y|ies) (negotiat\w*|recovery|compan\w*|servic\w*|intermediar\w*))\b",
 'Sign-off': r"(sincerely|regards|best wishes|thank you|yours)",
}
pos={k:[] for k in CUES}
for d,f,w,s in S:
    L=len(s)
    for k,c in CUES.items():
        flags=re.I|(re.M if k=='Greeting' else 0)
        if k=='Greeting':
            m=re.search(c,s[:L//10],re.I|re.M)  # opening tenth of the note
        elif k=='Sign-off':
            m=re.search(c,s[int(L*0.6):],re.I)
            if m: pos[k].append((int(L*0.6)+m.start())/L); continue
        else: m=re.search(c,s,re.I)
        if m: pos[k].append(m.start()/L)
for k,v in sorted(pos.items(),key=lambda kv: statistics.mean(kv[1]) if kv[1] else 9):
    print(f"{k:28s} n={len(v):2d} mean={statistics.mean(v):.2f} median={statistics.median(v):.2f}")
json.dump(pos, open("pos.json", "w"))
