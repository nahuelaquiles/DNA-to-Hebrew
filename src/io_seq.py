from pathlib import Path
import re

DNA_RE = re.compile(r"[^ACGTacgt]")

def load_dna_text(path: str) -> str:
    s = Path(path).read_text(encoding="utf-8", errors="ignore")
    # if FASTA, skip headers
    lines = []
    for line in s.splitlines():
        if line.startswith(">"):
            continue
        lines.append(line.strip())
    s = "".join(lines)
    s = DNA_RE.sub("", s).upper()
    return s

def revcomp(seq: str) -> str:
    comp = str.maketrans("ACGT", "TGCA")
    return seq.translate(comp)[::-1]
