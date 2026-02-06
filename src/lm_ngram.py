from collections import Counter
import math

class CharNGramLM:
    def __init__(self, n=4, k=0.5):
        self.n = n
        self.k = k
        self.counts = Counter()
        self.context_counts = Counter()
        self.vocab = set()

    def train(self, text: str):
        n = self.n
        pad = " " * (n-1)
        t = pad + text
        for i in range(len(t) - n + 1):
            ng = t[i:i+n]
            ctx = ng[:-1]
            ch = ng[-1]
            self.counts[(ctx, ch)] += 1
            self.context_counts[ctx] += 1
            self.vocab.add(ch)
        # Add space symbol to vocabulary (useful even if your output has no spaces)
        self.vocab.add(" ")

    def logprob(self, text: str) -> float:
        n = self.n
        V = max(1, len(self.vocab))
        pad = " " * (n-1)
        t = pad + text
        lp = 0.0
        for i in range(len(t) - n + 1):
            ng = t[i:i+n]
            ctx = ng[:-1]
            ch = ng[-1]
            c = self.counts.get((ctx, ch), 0)
            cc = self.context_counts.get(ctx, 0)
            p = (c + self.k) / (cc + self.k * V)
            lp += math.log(p)
        return lp
