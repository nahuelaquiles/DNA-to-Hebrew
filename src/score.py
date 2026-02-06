from typing import Set
import math


def load_wordlist(path: str) -> Set[str]:
    words: Set[str] = set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip()
            if not w:
                continue
            words.add(w)
    return words


def dict_hits_score(text: str, words: Set[str], min_len: int = 4) -> float:
    """Count matches of dictionary words in the text.
    Score weighted by square of word length to favor longer words."""
    n = len(text)
    score = 0.0
    for i in range(n):
        max_L = min(12, n - i)
        for L in range(min_len, max_L + 1):
            sub = text[i:i+L]
            if sub in words:
                score += (L * L)
    return score


def letter_balance_penalty(text: str) -> float:
    """Penalize overuse of any single letter (to avoid degenerate mappings)."""
    if not text:
        return 0.0
    from collections import Counter
    c = Counter(text)
    top = c.most_common(1)[0][1]
    frac = top / len(text)
    # If one letter accounts for >12% of the string, apply a penalty
    return max(0.0, (frac - 0.12) * 100.0)


def total_score(text: str, lm, words) -> float:
    """Combine language model score, dictionary hits, and penalties into a single score."""
    lm_score = lm.logprob(text)
    dh = dict_hits_score(text, words)
    pen = letter_balance_penalty(text)
    return (1.0 * lm_score) + (0.8 * dh) - (2.0 * pen)
