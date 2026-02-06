import random
from typing import Dict, List, Tuple


def random_mapping(symbols: List[str], hebrew_letters: List[str]) -> Dict[str, str]:
    """Return a random many-to-one mapping from symbols to Hebrew letters."""
    return {s: random.choice(hebrew_letters) for s in symbols}


def mutate(mapping: Dict[str, str], hebrew_letters: List[str], p_swap: float = 0.5) -> Dict[str, str]:
    """Generate a new mapping by either swapping two assignments or reassigning one symbol."""
    m = dict(mapping)
    keys = list(m.keys())
    if random.random() < p_swap:
        a, b = random.sample(keys, 2)
        m[a], m[b] = m[b], m[a]
    else:
        a = random.choice(keys)
        m[a] = random.choice(hebrew_letters)
    return m


def anneal(
    init_map: Dict[str, str],
    make_text_fn,
    score_fn,
    hebrew_letters: List[str],
    iters: int = 200000,
    T0: float = 1.0,
    Tf: float = 0.01,
    seed: int = 1,
) -> Tuple[Dict[str, str], float]:
    """Perform simulated annealing to optimize the mapping for highest score.

    Args:
        init_map: initial mapping from symbols to Hebrew letters.
        make_text_fn: function mapping a mapping to output string.
        score_fn: function to score the output string.
        hebrew_letters: list of possible Hebrew letters to assign.
        iters: number of iterations to run.
        T0: starting temperature.
        Tf: final temperature.
        seed: random seed for reproducibility.

    Returns:
        A tuple (best_mapping, best_score).
    """
    random.seed(seed)
    cur = dict(init_map)
    cur_text = make_text_fn(cur)
    cur_score = score_fn(cur_text)

    best = dict(cur)
    best_score = cur_score

    for t in range(1, iters + 1):
        # Exponential cooling schedule
        frac = t / iters
        T = T0 * ((Tf / T0) ** frac)

        cand = mutate(cur, hebrew_letters)
        cand_text = make_text_fn(cand)
        cand_score = score_fn(cand_text)

        delta = cand_score - cur_score
        # Accept new state if it's better or with Boltzmann probability
        if delta >= 0 or random.random() < pow(2.718281828, delta / max(1e-9, T)):
            cur, cur_text, cur_score = cand, cand_text, cand_score
            if cur_score > best_score:
                best, best_score = dict(cur), cur_score

    return best, best_score
