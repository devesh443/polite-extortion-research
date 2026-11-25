"""Shared helpers: read a note and draw the sample of 45 notes."""
import os, re

def read(path):
    b = open(path, "rb").read()
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16")
    try:
        return b.decode("utf-8-sig")
    except UnicodeDecodeError:
        return b.decode("latin-1")

def n_words(text):  # a word = a run of letters, apostrophes allowed
    return len(re.findall(r"[A-Za-z][A-Za-z']*", text))

def sample(root, verbose=False):
    """Return [(folder, file, words, text)] for the 45 sampled notes."""
    folders = sorted((d for d in os.listdir(root)
                      if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")), key=str.lower)
    eligible, no_txt, short = [], 0, 0
    for d in folders:
        txt = sorted((f for f in os.listdir(os.path.join(root, d)) if f.lower().endswith(".txt")), key=str.lower)
        if not txt:
            no_txt += 1; continue
        text = read(os.path.join(root, d, txt[0]))
        if n_words(text) < 100:
            short += 1; continue
        eligible.append((d, txt[0], n_words(text), text))
    picked = eligible[::4]
    if verbose:
        print(f"folders={len(folders)} no_txt={no_txt} short={short} eligible={len(eligible)} "
              f"sample={len(picked)} words={sum(x[2] for x in picked)}")
    return picked
