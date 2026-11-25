"""Draw Figs. 1-8. Run section_order.py first (it writes pos.json).
Run sample_notes.py, word_counts.py and section_order.py first: every number in the
figures is read from their outputs (sample_stats.json, word_counts.json, pos.json)
and from ransom_notes_coding_sheet.csv."""
import json, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Patch
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "Liberation Serif", "font.size": 8, "axes.titlesize": 8,
    "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.edgecolor": "#666666", "axes.linewidth": 0.6, "xtick.color": "#666666",
    "ytick.color": "#191919", "axes.labelcolor": "#191919", "savefig.dpi": 300,
    "hatch.linewidth": 0.6,
})
INK, INK2 = "#191919", "#666666"
DARK, MID, LIGHT = "#1b64be", "#519ced", "#9dc8f7"
ORANGE = "#f47230"
GRID = "#e3e3e3"
SC = 3.45   # single-column width (in)
DC = 7.0    # double-column width (in)
OUT = "fig"
import os; os.makedirs(OUT, exist_ok=True)

# ---------- data: everything below is computed from the pipeline outputs ----------
import csv
_rd = list(csv.DictReader(open("ransom_notes_coding_sheet.csv")))
ROWS = [r for r in _rd if r["No."].isdigit()]
ITEMS = list(ROWS[0].keys())[4:26]
N = len(ROWS)
def count(k): return sum(int(r[k]) for r in ROWS)
def pct(k): return round(100 * count(k) / N)
STATS = json.load(open("sample_stats.json"))
WC = json.load(open("word_counts.json"))

def clean(ax, grid_axis="x"):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(INK2)
    ax.tick_params(length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.5); ax.set_axisbelow(True)

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", pad_inches=0.03, facecolor="white")
    plt.close(fig)

# ---------- Fig 1: sampling flow ----------
fig, ax = plt.subplots(figsize=(SC, 2.1)); ax.axis("off"); ax.set_xlim(0, 10.5); ax.set_ylim(0, 10)
steps = [(f"{STATS['folders']} group folders in the archive", "sorted A\u2013Z, ignoring capitals"),
         (f"{STATS['with_txt']} folders with a .txt note", "first .txt file in each folder"),
         (f"{STATS['eligible']} notes of 100+ words", ""),
         (f"{STATS['sample']} notes, {STATS['sample']} groups", f"every fourth note \u00b7 {STATS['words']:,} words")]
drops = [f"\u2013 {STATS['no_txt']} folders with no .txt file", f"\u2013 {STATS['short']} notes under 100 words", "keep every fourth note"]
ys = [8.9, 6.25, 3.6, 0.95]
for i, ((t, s), y) in enumerate(zip(steps, ys)):
    fc = DARK if i == 3 else "white"; tc = "white" if i == 3 else INK
    ax.add_patch(FancyBboxPatch((0.1, y - 0.8), 6.0, 1.6, boxstyle="round,pad=0.02,rounding_size=0.25",
                                fc=fc, ec=DARK, lw=0.8))
    ax.text(3.1, y + (0.22 if s else 0), t, ha="center", va="center", color=tc, fontsize=7.5, weight="bold")
    if s: ax.text(3.1, y - 0.38, s, ha="center", va="center", color=("white" if i == 3 else INK2), fontsize=7)
    if i < 3:
        ax.add_patch(FancyArrowPatch((3.1, y - 0.85), (3.1, ys[i + 1] + 0.85), arrowstyle="-|>", mutation_scale=7, color=INK2, lw=0.8))
        ax.text(3.4, (y + ys[i + 1]) / 2, drops[i], ha="left", va="center", color=INK2, fontsize=7, style="italic")
save(fig, "fig1_sampling")

# ---------- Fig 2: sections ----------
sec = sorted(((k, count(k)) for k in ITEMS[:11]), key=lambda x: -x[1])
fig, ax = plt.subplots(figsize=(3.0, 2.45))
names = [s for s, _ in sec][::-1]; vals = [v for _, v in sec][::-1]
cols = [DARK if v >= 30 else LIGHT for v in vals]
ax.barh(names, vals, color=cols, height=0.62)
for i, v in enumerate(vals):
    ax.text(v + 0.6, i, f"{v} ({round(100*v/45)}%)", va="center", fontsize=7.5, color=INK)
ax.axvline(30, color=INK2, lw=0.6, ls=(0, (3, 2)))
ax.text(30, len(vals) - 0.35, "two-thirds of notes", fontsize=7, color=INK2, ha="center", va="bottom")
ax.set_xlim(0, 62); ax.set_xticks([0, 15, 30, 45]); ax.set_xlabel("Notes containing the section (of 45)")
ax.set_ylim(-0.6, len(vals) - 0.1)
clean(ax)
save(fig, "fig2_sections")

# ---------- Fig 3: typical order ----------
pos = json.load(open("pos.json"))
order = sorted(pos, key=lambda k: statistics.mean(pos[k]))
fig, ax = plt.subplots(figsize=(2.75, 2.6))
for i, k in enumerate(order[::-1]):
    v = pos[k]
    ax.scatter(v, [i] * len(v), s=7, color=LIGHT, edgecolors="none", zorder=2)
    m = statistics.mean(v)
    ax.scatter([m], [i], s=34, color=DARK, edgecolors="white", linewidths=0.8, zorder=3)
labels = [f"{k} (n={len(pos[k])})" for k in order[::-1]]
ax.set_yticks(range(len(order))); ax.set_yticklabels(labels)
ax.set_xlim(-0.02, 1.02); ax.set_xticks([0, .25, .5, .75, 1]); ax.set_xticklabels(["start", "¼", "½", "¾", "end"])
ax.set_xlabel("Where the section's first cue phrase falls in the note")
clean(ax)
h=[Line2D([],[],marker="o",ls="",color=DARK,markersize=5,label="mean position"),Line2D([],[],marker="o",ls="",color=LIGHT,markersize=3,label="one note")]
ax.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7, frameon=False, handletextpad=0.2)
save(fig, "fig3_order")

# ---------- Fig 4: business features ----------
_lab = {"Commercial vocabulary": "Commercial vocabulary", "Politeness markers": "Politeness markers",
        "Service vocabulary": "Service vocabulary", "Business motive or professional identity": "Business motive or identity",
        "Deletion or confidentiality promise": "Deletion or confidentiality promise",
        "Legal consequences": "Legal or regulatory consequences", "Security report": "Security report after payment",
        "Price stated": "Price stated in the note"}
feat = sorted(((lab, count(k)) for k, lab in _lab.items()), key=lambda x: -x[1])
fig, ax = plt.subplots(figsize=(2.75, 2.05))
n = [a for a, _ in feat][::-1]; v = [b for _, b in feat][::-1]
ax.barh(n, v, color=DARK, height=0.62)
for i, x in enumerate(v): ax.text(x + 0.6, i, f"{x} ({round(100*x/45)}%)", va="center", fontsize=7.5)
ax.set_xlim(0, 54); ax.set_xticks([0, 15, 30, 45]); ax.set_xlabel("Notes with the feature (of 45)"); ax.set_ylim(-0.6, len(v) - 0.4)
clean(ax)
save(fig, "fig4_business")

# ---------- Fig 5: distributions ----------
secs = [sum(int(r[k]) for k in ITEMS[:11]) for r in ROWS]; idx = [int(r["Business-writing index (0-5)"]) for r in ROWS]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(SC, 1.6), gridspec_kw={"wspace": 0.35})
for ax, data, rng, lab, title in [(a1, secs, range(2, 11), "Sections (of 11)", "(a) Sections per note"),
                                  (a2, idx, range(0, 6), "Index score (of 5)", "(b) Business-writing index")]:
    c = [data.count(k) for k in rng]
    ax.bar(list(rng), c, color=DARK, width=0.7)
    for k, y in zip(rng, c):
        if y: ax.text(k, y + 0.2, str(y), ha="center", va="bottom", fontsize=7)
    ax.set_xticks(list(rng)); ax.set_xlabel(lab); ax.set_title(title, fontsize=7.5, color=INK, pad=4)
    ax.set_ylim(0, max(c) + 2.2); ax.set_yticks([]); clean(ax, None); ax.spines["left"].set_visible(False)
a1.set_ylabel("Notes")
save(fig, "fig5_distributions")

# ---------- Fig 6: words ----------
_w = ["you / your / yours", "we / our / us", "will / won't", "if", "do not / don't", "pay (all forms)",
      "please", "ransom", "thank", "sorry / apologise"]
words = sorted(((k, WC[k]["notes"]) for k in _w), key=lambda x: -x[1])
fig = plt.figure(figsize=(SC, 3.3))
a1 = fig.add_axes([0.36, 0.43, 0.6, 0.55]); a2 = fig.add_axes([0.36, 0.0, 0.6, 0.27])
n = [a for a, _ in words][::-1]; v = [b for _, b in words][::-1]
hl = {"ransom", "pay (all forms)"}
a1.barh(n, v, color=[DARK if x in hl else LIGHT for x in n], height=0.62)
for i, x in enumerate(v): a1.text(x + 0.6, i, str(x), va="center", fontsize=7.5)
a1.set_xlim(0, 50); a1.set_title("(a) Notes containing the word (of 45)", fontsize=7.5, loc="left", x=-0.55, pad=4)
clean(a1); a1.set_ylim(-0.6, len(v) - 0.4)
pairs = [("The demand", "ransom", WC["ransom"]["notes"], "pay (all forms)", WC["pay (all forms)"]["notes"]),
         ("The theft", "stole, stolen", WC["stole / stolen"]["notes"], "downloaded, exfiltrated, copied",
          WC["downloaded / exfiltrated / copied"]["notes"])]
yy = [1, 0]
for (lab, w1, c1, w2, c2), y in zip(pairs, yy):
    a2.barh(y + 0.19, c1, height=0.34, color=ORANGE)
    a2.barh(y - 0.19, c2, height=0.34, color=DARK)
    a2.text(c1 + 0.5, y + 0.19, f"{c1}  {w1}", va="center", fontsize=7.3)
    a2.text(c2 + 0.5, y - 0.19, f"{c2}  {w2}", va="center", fontsize=7.3)
a2.set_yticks(yy); a2.set_yticklabels([p[0] for p in pairs]); a2.set_xlim(0, 50)
a2.set_title("(b) Naming the act: plain word vs. softer word", fontsize=7.5, loc="left", x=-0.55, pad=4)
a2.set_xlabel("Notes (of 45)"); clean(a2); a2.set_ylim(-0.5, 1.5)

save(fig, "fig6_words")

# ---------- Fig 7: politeness vs threat ----------
def _split(cond):
    a = [r for r in ROWS if cond(r)]; b = [r for r in ROWS if not cond(r)]
    return (sum(int(r["Threat"]) for r in a), len(a)), (sum(int(r["Threat"]) for r in b), len(b))
groups = [("Politeness markers",) + _split(lambda r: r["Politeness markers"] == "1"),
          ("Reassurance",) + _split(lambda r: r["Reassurance"] == "1"),
          ("Index 3 or more",) + _split(lambda r: int(r["Business-writing index (0-5)"]) >= 3)]
fig, ax = plt.subplots(figsize=(SC, 1.7))
for i, (g, (a, an), (b, bn)) in enumerate(groups):
    y = len(groups) - 1 - i
    ax.barh(y + 0.19, 100 * a / an, height=0.34, color=DARK)
    ax.barh(y - 0.19, 100 * b / bn, height=0.34, color="white", edgecolor=DARK, hatch="////", lw=0.6)
    ax.text(100 * a / an + 1, y + 0.19, f"{round(100*a/an)}%  ({a}/{an})", va="center", fontsize=7.3)
    ax.text(100 * b / bn + 1, y - 0.19, f"{round(100*b/bn)}%  ({b}/{bn})", va="center", fontsize=7.3)
ax.set_yticks(range(len(groups))); ax.set_yticklabels([g[0] for g in groups][::-1])
ax.set_xlim(0, 125); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("Share of notes that state a threat (%)")
clean(ax)
h=[Patch(facecolor=DARK,label="notes with the feature"),Patch(facecolor="white",edgecolor=DARK,hatch="////",label="notes without it")]
ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2, fontsize=7, frameon=False)
save(fig, "fig7_politeness")

# ---------- Fig 8: sales letter vs ransom note ----------
rows = [("Establishing credentials", "Business motive or professional identity", [pct("Business motive or professional identity")]),
        ("Introducing the offer", "Reassurance that the problem can be solved", [pct("Reassurance")]),
        ("Offering incentives", "Proof or guarantee \u00b7 deletion/confidentiality promise \u00b7 security report",
         [pct("Proof or guarantee"), pct("Deletion or confidentiality promise"), pct("Security report")]),
        ("Enclosing documents", "File lists and samples (part of the proof)", None),
        ("Soliciting a response", "Contact instructions", [pct("Contact instructions")]),
        ("Using pressure tactics", "Threat \u00b7 deadline", [pct("Threat"), pct("Deadline")]),
        ("Ending politely", "Sign-off", [pct("Sign-off")])]
extra = [("Announcing the attack", pct("Announcement")), ("Technical warnings", pct("Technical warnings")),
         ("Discouraging outside help", pct("Discouraging outside help"))]
fig, ax = plt.subplots(figsize=(DC, 3.05)); ax.axis("off")
W = 100; ax.set_xlim(0, W); H = len(rows) + 2.6; ax.set_ylim(-0.2, H)
xL, wL = 0.5, 21; xR, wR = 27.5, 48.5; xB, wB = 77.5, 22
ax.text(xL + wL / 2, H - 0.35, "Sales promotion letter (Bhatia)", ha="center", fontsize=8, weight="bold")
ax.text(xR + wR / 2, H - 0.35, "Equivalent in the ransom notes", ha="center", fontsize=8, weight="bold")
ax.text(xB + wB / 2, H - 0.35, "Share of the 45 notes", ha="center", fontsize=8, weight="bold")
for i, (m, eq, pct) in enumerate(rows):
    y = H - 1.35 - i
    ax.add_patch(FancyBboxPatch((xL, y - 0.36), wL, 0.72, boxstyle="round,pad=0,rounding_size=0.18", fc="white", ec=INK2, lw=0.6))
    ax.text(xL + wL / 2, y, m, ha="center", va="center", fontsize=7.5)
    ax.add_patch(FancyArrowPatch((xL + wL + 0.4, y), (xR - 0.4, y), arrowstyle="-|>", mutation_scale=6, color=INK2, lw=0.6))
    ax.add_patch(FancyBboxPatch((xR, y - 0.36), wR, 0.72, boxstyle="round,pad=0,rounding_size=0.18", fc="#eaf3fd", ec=DARK, lw=0.6))
    ax.text(xR + 1.2, y, eq, ha="left", va="center", fontsize=7.5 if len(eq)<60 else 6.6)
    if pct:
        bw = wB / len(pct)
        for j, p in enumerate(pct):
            x0 = xB + j * bw
            ax.add_patch(Rectangle((x0, y - 0.22), (bw - 0.8), 0.44, fc="#eef0f3", ec="none"))
            ax.add_patch(Rectangle((x0, y - 0.22), (bw - 0.8) * p / 100, 0.44, fc=DARK, ec="none"))
            ax.text(x0 + (bw - 0.8) * p / 100 + 0.5 if p < 70 else x0 + 0.6, y, f"{p}%", va="center",
                    fontsize=7.3, color=(INK if p < 70 else "white"))
    else:
        ax.text(xB, y, "counted in the proof above", va="center", fontsize=7.3, color=INK2, style="italic")
yb = 0.45
ax.text(xL, yb + 0.05, "No sales-letter equivalent:", va="center", fontsize=7.5, weight="bold")
bx = xR
for t, p in extra:
    w = 22.2
    ax.add_patch(FancyBboxPatch((bx, yb - 0.36), w, 0.72, boxstyle="round,pad=0,rounding_size=0.18", fc=DARK, ec=DARK, lw=0.6))
    ax.text(bx + w / 2, yb + 0.03, f"{t} · {p}%", ha="center", va="center", fontsize=6.3, color="white")
    bx += w + 0.8
ax.plot([0.5, 99.5], [1.15, 1.15], color=GRID, lw=0.8)
save(fig, "fig8_sales_letter")
print("ok")
