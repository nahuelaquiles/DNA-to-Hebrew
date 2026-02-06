import random


def shuffle_seq(seq: str, seed: int = 1) -> str:
    """Return a shuffled version of the input sequence preserving nucleotide frequencies.

    Args:
        seq: The input DNA sequence to shuffle.
        seed: Random seed for reproducibility.

    Returns:
        A new sequence where the characters are randomly permuted.
    """
    random.seed(seed)
    s = list(seq)
    random.shuffle(s)
    return "".join(s)
