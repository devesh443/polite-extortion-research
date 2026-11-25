# Polite Extortion: Ransomware Notes as a Form of Business Writing

Supplementary materials for the research paper **"Polite Extortion: Ransomware Notes as a Form of Business Writing"** (English Experiential Learning Project). The paper itself is not included here. Appendix C of the paper describes these supplementary files.

This repository contains the coding sheet and the Python scripts. With them, anyone can rebuild the 45-note sample from the public archive and reproduce the sampling counts, coded-item counts, word counts, section-order positions and Figs. 1–8 reported in the paper. A few details in the paper's text come from reading the notes rather than from the scripts: for example, the deadline lengths, the number of letter-style closings, and how a word is used in context (the script finds *team* in 11 notes; the paper's figure of nine counts only the notes where it refers to the writers). Figures quoted from other studies are not reproduced here.

## Contents

- [Project overview](#project-overview)
- [Research objectives](#research-objectives)
- [Data source](#data-source)
- [Sampling method](#sampling-method)
- [Repository structure](#repository-structure)
- [Requirements and installation](#requirements-and-installation)
- [Reproducing the analysis](#reproducing-the-analysis)
- [Key findings](#key-findings)
- [Use of AI tools](#use-of-ai-tools)
- [Limitations](#limitations)
- [Safety and privacy](#safety-and-privacy)
- [Attribution and licence of the source data](#attribution-and-licence-of-the-source-data)

## Project overview

When ransomware locks a victim's files, the attackers leave a note that says what happened and how to pay. This project reads that note as a piece of professional writing. It asks how much of the note is borrowed from business and customer-service communication.

The study is a text-based content analysis of 45 English-language ransom notes, one from each of 45 ransomware groups, selected by a fixed rule from the public archive maintained by Zscaler ThreatLabz.

- Each note was coded on a 22-item yes/no codebook: eleven structural sections (moves) and eleven language features.
- Word frequencies were counted over the sample of about 11,600 words.
- The usual order of sections was estimated from where cue phrases fall in each note.
- The results are interpreted using genre analysis (Swales, Bhatia), speech act theory (Austin, Searle, Fraser), politeness theory (Brown and Levinson) and persuasion principles (Cialdini).

Only the written text was analysed. No malware was downloaded or run, and no links or contact addresses in the notes were opened.

## Research objectives

1. Identify the usual sections of a ransomware note and the order they come in.
2. Measure how often features of business and customer-service writing occur.
3. See how the notes mix politeness and reassurance with threats and deadlines.
4. Describe how the writers present themselves and how they address the victim.

## Data source

| Item | Detail |
|---|---|
| Archive | Zscaler ThreatLabz, *Ransomware notes* — <https://github.com/ThreatLabz/ransomware_notes> |
| Commit | [`8765d0b53dc09571b217a3fa3365730c46be9dee`](https://github.com/ThreatLabz/ransomware_notes/tree/8765d0b53dc09571b217a3fa3365730c46be9dee) (13 August 2026) |
| Accessed | 8 October 2026 |
| Size at that commit | 222 group folders |
| Licence | MIT License, Copyright (c) 2022 Zscaler ThreatLabz |

All results depend on this exact commit. Later commits may add or change notes, and the same rule would then select a different sample. The archive is **not** copied into this repository; the instructions below clone it at the pinned commit.

## Sampling method

The sample was drawn by a fixed, deterministic rule so that notes were not chosen for being interesting. The rule is implemented in `notes.py` (`sample()`):

1. List the group folders in the archive (hidden folders excluded) and sort them alphabetically, ignoring capitals.
2. In each folder, take the `.txt` file that comes first in alphabetical order of file name (again ignoring capitals) as that group's note. Folders without a `.txt` file are skipped.
3. Drop notes of fewer than 100 words. A word is any run of letters, apostrophes allowed (`[A-Za-z][A-Za-z']*`).
4. From the remaining notes, keep every fourth one, starting with the first.

| Step | Count |
|---|---|
| Group folders in the archive | 222 |
| Folders with no `.txt` file | −21 |
| Folders with a `.txt` note | 201 |
| Notes under 100 words | −22 |
| Eligible notes (100+ words) | 179 |
| **Sample (every fourth note)** | **45 notes from 45 groups, 11,647 words** |

The sampled notes range from 102 to 627 words (median 225). The full list is in the coding sheet and in Appendix A (Table II) of the paper.

## Repository structure

```text
polite-extortion-research/
├── README.md                        This file
├── requirements.txt                 Python dependency (matplotlib, for the figures only)
├── .gitignore                       Excludes the cloned archive, generated outputs and local files
├── ransom_notes_coding_sheet.csv    Coding of all 45 notes on the 22 codebook items
├── notes.py                         Shared helper: reads a note and draws the 45-note sample
├── sample_notes.py                  Sampling flow and sample list (Fig. 1, Table II)
├── word_counts.py                   Word-frequency counts (Section IV, Fig. 6)
├── section_order.py                 Cue-phrase positions for section order (Fig. 3, Table V)
├── analyse_coding.py                Counts and cross-tabulations from the coding sheet
└── make_figures.py                  Draws Figs. 1–8
```

| File | Input | Output |
|---|---|---|
| `ransom_notes_coding_sheet.csv` | — | One row per note: number, group folder, file name, word count, the 22 items (1 = present, 0 = absent) and the business-writing index (0–5). The last row holds column totals. |
| `notes.py` | — | Imported by the three archive scripts; not run directly. |
| `sample_notes.py` | archive path | Prints the sampling counts and the 45 notes; writes `sample_stats.json`. |
| `word_counts.py` | archive path | Prints occurrences and number of notes for each word group; writes `word_counts.json`. |
| `section_order.py` | archive path | Prints the number of notes with a cue phrase and the mean and median position for each section; writes `pos.json`. |
| `analyse_coding.py` | coding sheet | Prints item counts, sections per note, index summaries (scores of 3 or more, 5 and 0), threat cross-tabulations, median length and legal consequences by index group, and word-count summaries. It also checks that every index value matches its definition. |
| `make_figures.py` | coding sheet and the three JSON files | Writes `fig/fig1_sampling.png` … `fig/fig8_sales_letter.png`. |

The generated files (`*.json`, `fig/`) are not committed. They are rebuilt by the scripts.

### Coding sheet columns

- **Sections (11):** Greeting, Announcement, Data theft claim, Reassurance, Proof or guarantee, Contact instructions, Deadline, Threat, Technical warnings, Discouraging outside help, Sign-off.
- **Language features (11):** Service vocabulary, Commercial vocabulary, Business motive or professional identity, Deletion or confidentiality promise, Security report, Legal consequences, Price stated, Politeness markers, Numbered lists, Question headings, Language errors.
- **Business-writing index (0–5):** one point each for service vocabulary, commercial vocabulary, business motive or professional identity, a deletion/confidentiality promise *or* a security report, and politeness markers.

The full codebook definitions and the cue phrases are in Appendix B (Tables III–V) of the paper.

**Coding correction.** The Blacklock note was first marked 1 for commercial vocabulary. It contains none of the codebook's words for that item (buy, purchase, price, cost, fee, deal, agreement, negotiate, offer, terms). It is now marked 0, and its index is 4.

## Requirements and installation

- **Python 3.7 or later.** `make_figures.py` needs matplotlib 3.5 or later, which needs Python 3.7 or later; recent matplotlib releases need a newer Python (matplotlib 3.11.2 needs Python 3.11 or later). Verified with Python 3.14.10 and matplotlib 3.11.2.
- **matplotlib** is needed for `make_figures.py` only. The other five scripts use the standard library. Verified with matplotlib 3.11.2.
- **Git**, to clone the source archive.
- **Liberation Serif font** (optional, for an exact visual match). `make_figures.py` sets this font. Without it, matplotlib falls back to its default font and prints many `findfont` warnings. The numbers in the figures stay the same, but the wider fallback font makes some labels overflow their boxes in Figs. 1 and 8.
  - Debian/Ubuntu: `sudo apt install fonts-liberation`
  - Other systems: download the TTF archive from the [Liberation Fonts releases](https://github.com/liberationfonts/liberation-fonts/releases) and install the `LiberationSerif-*.ttf` files (on Windows: right-click > Install). If matplotlib still cannot find the font, delete its font cache and run the script again.

Set up the project:

```bash
git clone https://github.com/devesh443/polite-extortion-research.git
cd polite-extortion-research

python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell). If activation fails with "running scripts is disabled
# on this system", first run (affects only the current PowerShell window):
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
# .venv\Scripts\Activate.ps1
# Windows (Git Bash):
# source .venv/Scripts/activate

pip install -r requirements.txt
```

> On Windows, use `python` rather than `python3`. The `python3` command may open the Microsoft Store instead of running Python.

## Reproducing the analysis

Run every command from the repository root; the scripts read and write files in the current directory. Run them in this order, because `make_figures.py` reads the outputs of the first three scripts.

**1. Get the source archive at the pinned commit**

```bash
git clone https://github.com/ThreatLabz/ransomware_notes
git -C ransomware_notes checkout 8765d0b53dc09571b217a3fa3365730c46be9dee
```

**2. Run the pipeline**

```bash
python sample_notes.py ransomware_notes    # sampling flow and the 45 notes (Fig. 1, Table II) -> sample_stats.json
python word_counts.py ransomware_notes     # word counts (Section IV, Fig. 6)                   -> word_counts.json
python section_order.py ransomware_notes   # cue-phrase positions (Fig. 3, Table V)             -> pos.json
python analyse_coding.py                   # counts and cross-tabulations from the coding sheet
python make_figures.py                     # Figs. 1-8                                           -> fig/
```

**3. Check the output**

The first line printed by `sample_notes.py` should be:

```text
folders=222 no_txt=21 short=22 eligible=179 sample=45 words=11647
```

It then prints the sample list: 45 tab-separated lines (number, group folder, file name, word count), which should match the first four columns of the 45 numbered rows of `ransom_notes_coding_sheet.csv` exactly. If the first line differs, the archive is not at the pinned commit or files are missing from it (see *Antivirus software* below), and the results will not match the paper.

`analyse_coding.py` should report, among other lines:

```text
Sections per note: mean 6.4, min 2, max 10
Index: >=3 in 19 notes, 5 in ['ailock', 'novagroup'], 0 in 7
Any of the three business features: 37; all three: 6
Threat | politeness markers: with 16/20, without 22/25
Words: total 11647, min 102, max 627, median 225
```

`make_figures.py` prints `ok` when all eight figures have been written.

### Reproducibility notes

- **Determinism.** The sample and all outputs are fully determined by the archive commit. Repeated runs produce byte-identical files.
- **Line endings (Fig. 3 only).** `section_order.py` measures positions as character offsets. Git for Windows (with its default `core.autocrlf=true`) checks out notes stored with LF endings as CRLF, while macOS and Linux keep them as LF. This applies to 27 of the 45 sampled notes; the other 18 have the same bytes on every system. It shifts individual positions in `pos.json` slightly (by at most about 0.004) and can change some medians printed by the script in the second decimal place. The counts and mean positions in Table V are the same either way. The paper's figures were reproduced on a Windows (CRLF) checkout.
- **Antivirus software.** The archive holds the text of real ransom notes. Some antivirus products, including Microsoft Defender, may flag and quarantine some of these text and HTML files when the archive is cloned, copied or read. On Windows this was observed for files in the `lockbit`, `ftcode`, `blackhunt`, `trigona`, `helldown` and `akira` folders. The scripts only read the files as text and never run them. Losing a file that is not the first `.txt` in its folder makes no difference. Losing a folder's first `.txt` note, however, changes the sample, because every fourth eligible note is taken. For example, if `helldown/Readme.[id].txt` is removed, `sample_notes.py` prints `no_txt=22 ... eligible=178 ... words=11193` and 26 of the 45 notes change. Always compare the first line printed by `sample_notes.py` with the expected line above, and check `git -C ransomware_notes status` for deleted files. If files are missing, restore them (`git -C ransomware_notes checkout -- .`) after allowing them in your antivirus software, or run the pipeline on a system where they are not removed. Do not open or run anything in the archive.
- **Encoding.** `notes.py` detects UTF-16 only when the file starts with a byte-order mark. Two first-in-folder notes that are not in the sample (`kawalocker` and `safepay`) are UTF-16 without a byte-order mark, so their word counts are inflated. Both still have well over 100 words, so this does not affect the sample.

## Key findings

All figures below come from the coding sheet and the scripts in this repository.

**Structure (objective 1)**
- A stable core of five sections: contact instructions (45 of 45 notes, 100%), announcement of the attack (43, 96%), threat (38, 84%), data theft claim (33, 73%) and technical warnings (30, 67%).
- A note has on average 6.4 of the eleven sections (minimum 2, maximum 10).
- The sections follow a broadly similar order: greeting, announcement and data theft claim first; reassurance, contact instructions, proof and the threat about a third of the way in; the deadline near the middle; warnings against outside help and technical warnings later; and a sign-off at the end. Individual notes depart from this order quite a lot.
- 30 notes (67%) use numbered or lettered lists, and 17 (38%) have question headings such as "What happened?".

**Business and service language (objective 2)**
- 37 notes (82%) use commercial vocabulary, service vocabulary or a stated business motive; 6 (13%) have all three. Commercial vocabulary appears in 31 notes (69%), service vocabulary in 18 (40%).
- Only 4 notes state a price. The rest ask the reader to make contact first.
- On the business-writing index (0–5), 19 notes (42%) score three or more, two (AiLock and Nova Group) score five, and 7 (16%) score zero.
- *Ransom* appears in only 5 of the 45 notes, while some form of *pay* appears in 23. *Stole/stolen* appears in 9 notes, against 19 for the more neutral *downloaded*, *exfiltrated* or *copied*.

**Politeness, reassurance and threat (objective 3)**
- Politeness markers appear in 20 notes (44%) and reassurance in 22 (49%).
- Politeness does not replace the threat: 80% of notes with politeness markers (16/20) state a threat, against 88% of those without (22/25).
- 19 notes (42%) set a deadline, and 13 (29%) tell the reader not to seek outside help.

**Self-presentation and address (objective 4)**
- The writers nearly always speak as a group (*we/our/us* in 44 notes); 16 notes claim a business motive or professional identity.
- The reader is addressed directly throughout: *you/your/yours* occur 723 times.

**Overall.** The ransom note behaves as a hybrid genre: it is organised like a sales letter but still works as a threat. The business register makes paying look like an ordinary commercial decision rather than giving in to extortion.

## Use of AI tools

- **Coding.** An AI assistant (Claude, by Anthropic) applied the written codebook to the full text of all 45 notes and marked each item 1 or 0. An item was marked 1 only if the note clearly met the definition; doubtful cases were marked 0. The exact model version and the prompt used for the coding were not kept, so they are not included here.
- **Correction.** One coding decision (Blacklock, commercial vocabulary) was later corrected because it did not match the codebook's word list.
- **Writing and figures.** The AI assistant was also used for help in drafting and revising the paper's text and in preparing the figures.
- **This repository.** The repository was prepared with the help of an AI coding assistant (Claude Code). It checked that the scripts run, re-ran the full pipeline against the pinned commit, compared the outputs with the paper and wrote this README. The research data and scripts were not changed.
- **Word counts.** `word_counts.py` was rewritten when these supplementary files were prepared, and the paper's word counts were updated to match its output.
- **No human validation.** The coding has **not** been checked independently by a second human coder. No inter-coder reliability figure exists.

## Limitations

- **No independent human coding validation.** The coding was done once by an AI tool following the written codebook. No second coder checked it, which matters most for items that need judgement, such as reassurance.
- **Single archive.** All notes come from one archive, so the sample reflects what one research team collected and may not be typical of ransomware in general.
- **No dates.** The archive does not date its notes, so changes in the business style over time cannot be assessed.
- **Inclusion rules.** Only English `.txt` notes of 100 words or more were included; shorter notes may be plainer. One note was taken per group, although some groups have several versions.
- **Section order is an estimate.** It is based on cue phrases, which are narrower than the coding definitions.
- **Text only.** The study cannot say how real readers react to the notes or whether the attackers keep their promises.
- **Small sample** (a note for this repository, not one of the limitations listed in the paper). With 45 notes, the counts and cross-tabulations are descriptive; the paper reports no statistical significance tests.

## Safety and privacy

- This repository contains **no ransom-note texts, no malware and no contact details** from the notes (no URLs, onion addresses, email addresses, chat IDs or payment addresses).
- The coding sheet lists only group folder names, file names, word counts and 0/1 codes. File names are reproduced exactly as they appear in the public archive, so that the sample can be rebuilt. Placeholders such as `[id]`, `[rand]` and `[key]` were already used in those names by ThreatLabz in place of the original identifiers.
- No personal information about victims, students or researchers is included.

## Attribution and licence of the source data

The ransom notes analysed here come from the **Ransomware notes** archive by **Zscaler ThreatLabz**: <https://github.com/ThreatLabz/ransomware_notes> (commit `8765d0b53dc09571b217a3fa3365730c46be9dee`). The archive is released under the MIT License, Copyright (c) 2022 Zscaler ThreatLabz. Group names in this repository are the archive's folder names.

This repository does not redistribute any files from the archive. Users who clone the archive are bound by its licence. ThreatLabz is not affiliated with this project and has not reviewed or endorsed it.

If you use these materials, please cite the paper and the ThreatLabz archive:

> Zscaler ThreatLabz, "Ransomware notes," GitHub repository, 2026. [Online]. Available: https://github.com/ThreatLabz/ransomware_notes
