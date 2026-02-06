import argparse
from io_seq import load_dna_text, revcomp
from genetic_code import CODON2AA, AA_SYMBOLS
from hebrew_norm import norm_hebrew
from lm_ngram import CharNGramLM
from score import load_wordlist, total_score
from anneal import random_mapping, anneal
from null_models import shuffle_seq


def dna_to_aa(seq: str, frame: int) -> str:
    """Translate a DNA sequence into an amino acid sequence in the given reading frame."""
    aa = []
    for i in range(frame, len(seq) - 2, 3):
        cod = seq[i:i+3]
        aa.append(CODON2AA.get(cod, "X"))
    return "".join([c for c in aa if c != "X"])


def make_text_from_aa(aa_seq: str, mapping: dict) -> str:
    """Convert an amino acid sequence to a Hebrew letter string using a mapping."""
    return "".join(mapping.get(sym, "") for sym in aa_seq)


def main():
    ap = argparse.ArgumentParser(description="Search for hidden Hebrew-like messages in DNA sequences.")
    ap.add_argument("--dna", required=True, help="Path to DNA file (txt or FASTA)")
    ap.add_argument("--hebrew_words", required=True, help="Path to Hebrew wordlist file")
    ap.add_argument("--hebrew_corpus", required=True, help="Path to Hebrew corpus for language model")
    ap.add_argument("--iters", type=int, default=200000, help="Iterations for simulated annealing")
    ap.add_argument("--seed", type=int, default=1, help="Random seed for reproducibility")
    ap.add_argument("--null", action="store_true", help="Shuffle DNA before analysis (control)")
    args = ap.parse_args()

    dna = load_dna_text(args.dna)
    if args.null:
        dna = shuffle_seq(dna, seed=args.seed)

    # Prepare language model from Hebrew corpus
    corpus = open(args.hebrew_corpus, "r", encoding="utf-8", errors="ignore").read()
    corpus = norm_hebrew(corpus, unify_finals=True)
    lm = CharNGramLM(n=4, k=0.5)
    lm.train(corpus)

    # Load dictionary of Hebrew words
    words = load_wordlist(args.hebrew_words)

    heb_letters = list("אבגדהוזחטיכלמנסעפצקרשת")

    best_global = None
    best_score = float("-inf")
    best_meta = None

    # Evaluate forward and reverse complement sequences across three reading frames
    for orient in ["fwd", "rev"]:
        seq = dna if orient == "fwd" else revcomp(dna)
        for frame in [0, 1, 2]:
            aa_seq = dna_to_aa(seq, frame=frame)
            init = random_mapping(AA_SYMBOLS, heb_letters)

            def make_text_fn(m):
                return make_text_from_aa(aa_seq, m)

            def score_fn(txt):
                return total_score(txt, lm, words)

            best_map, sc = anneal(
                init,
                make_text_fn,
                score_fn,
                heb_letters,
                iters=args.iters,
                seed=args.seed,
            )
            if sc > best_score:
                best_score = sc
                best_global = best_map
                best_meta = (orient, frame, len(aa_seq))

    # Reconstruct output using the best mapping and orientation
    orient, frame, _ = best_meta
    seq = dna if orient == "fwd" else revcomp(dna)
    aa_seq = dna_to_aa(seq, frame=frame)
    out = make_text_from_aa(aa_seq, best_global)
    print("BEST:", best_meta, "score=", best_score)
    print("OUTPUT_PREVIEW:", out[:500])
    print("MAPPING:", best_global)


if __name__ == "__main__":
    main()
