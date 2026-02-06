# DNA-to-Hebrew

This repository contains a Python-based pipeline to search for hidden messages in DNA sequences by mapping amino acids (or codons) to letters of the Hebrew alphabet. The project is an ongoing exploration of whether coherent Hebrew words or phrases can be decoded from human genomic sequences.

## Overview

1. **DNA reading**: The code reads DNA sequences (FASTA or raw text) and translates them into amino acids using the standard genetic code.
2. **Mapping amino acids to Hebrew letters**: Each amino acid (plus STOP) is mapped to one of the 22 Hebrew letters. The mapping is optimized using simulated annealing or genetic algorithms to maximize coherence of the resulting text.
3. **Language model and dictionary scoring**: The decoded Hebrew text is evaluated using a Hebrew n‑gram language model and a dictionary of Hebrew words. The score measures how "word-like" the translation is.
4. **Null model controls**: Control runs with shuffled DNA sequences are included to determine whether any detected signal is significantly above random chance.
5. **Outputs**: Results are stored in the `outputs/` directory. They include best mappings, scores, and previews of the translated sequences.

## Repository structure

- `data/`
  - `sequences/`: Place your DNA sequences here (one sequence per file, raw or FASTA). Two example files (`seqA.txt` and `seqB.txt`) can be added for testing.
  - `dictionaries/`: Contains a Hebrew word list (`hebrew_words.txt`).
  - `corpora/`: Contains a large Hebrew text corpus (`hebrew_corpus.txt`) used to train the language model.
- `src/`: Python source code for loading sequences, normalizing Hebrew text, training the n‑gram model, scoring, and optimization algorithms.
- `outputs/`: Where results and logs will be written.
- `README.md`: Project description and instructions.

## Getting started

### 1. Install Python

Make sure you have Python 3.8 or higher installed. You can download it from https://www.python.org/downloads/.

### 2. Clone the repository

Use `git` to clone this repository to your local computer:

```bash
git clone https://github.com/nahuelaquiles/DNA-to-Hebrew.git
cd DNA-to-Hebrew
```

If you are new to git, follow [GitHub’s documentation](https://docs.github.com/en/get-started/quickstart/set-up-git) to set up Git on your computer.

### 3. Set up the environment

Install required Python packages. For the minimal working version, there are no external dependencies beyond the Python standard library. Later extensions may require packages like `numpy` or `biopython`.

Optionally, you can create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Then install dependencies (if any):

```bash
pip install -r requirements.txt
```

Currently, `requirements.txt` is empty; you can skip this step.

### 4. Prepare data

Download or place your DNA sequences in `data/sequences/`. Each file should contain only A, C, G, and T characters, or you can include FASTA headers starting with `>`.

Prepare a dictionary of Hebrew words (`hebrew_words.txt`) and a large Hebrew text corpus (`hebrew_corpus.txt`) in `data/dictionaries/` and `data/corpora/`, respectively. You may obtain these from open sources like Hebrew Wikipedia or Biblical texts. Ensure the text is normalized (no vowels or niqqud).

### 5. Run the pipeline

Use the main script in `src/run.py`. For example:

```bash
python -m src.run \
  --dna data/sequences/seqA.txt \
  --hebrew_words data/dictionaries/hebrew_words.txt \
  --hebrew_corpus data/corpora/hebrew_corpus.txt \
  --iters 400000 \
  --seed 1
```

- `--dna`: Path to the DNA sequence file.
- `--hebrew_words`: Path to the Hebrew word list.
- `--hebrew_corpus`: Path to the Hebrew corpus for training the n‑gram model.
- `--iters`: Number of simulated annealing iterations (e.g., 200000 or 400000).
- `--seed`: Random seed for reproducibility.
- `--null`: If you add `--null`, the DNA will be shuffled to provide a null model control.

The script will output the best mapping and a preview of the decoded text. Higher scores compared to the null model may indicate non-random Hebrew-like structure.

### 6. Interpret results

Interpretation requires caution. Significant signals should be validated with additional controls to avoid false positives. See the project’s documentation for details.

## Next steps

This project is in early development. Future work includes:

- Implementing codon‑to‑Hebrew mapping.
- Support for variable-length encoding schemes.
- Use of neural language models.
- Automated statistical significance tests.

Contributions are welcome! Please open an issue or pull request if you wish to improve the code.
