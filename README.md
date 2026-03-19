# LLMs on Lexicalized Noun-Noun Compounds: Mamba vs. Transformer & Multilingual vs. Monolingual

A replication and extension of [Rambelli et al. (2024)](https://aclanthology.org/2024.acl-long.637/), investigating how different language model architectures interpret implicit semantic relations in lexicalized noun-noun compounds (e.g., *birthday cake* → "a cake **for** birthdays").

## Overview

This project addresses two research questions:

1. **Can attention-free Mamba models perform as well as transformer LLMs** on implicit relation prediction in English noun-noun compounds?
2. **Do bilingual/multilingual BERT models perform equally well across languages**, compared to their monolingual counterparts — specifically in English and Mandarin Chinese?

## Highlights

- **Self-created Chinese dataset**: Manually annotated 176 Mandarin Chinese lexicalized noun-noun compounds using the Hatcher-Bourque classification system (Pepper, 2022), including custom Chinese paraphrase templates designed to be linguistically natural across 9 semantic relations.
- **Multi-model evaluation**: Ran experiments on `Falcon-7B`, `Falcon-Mamba-7B`, `Mistral-7B`, and their instruct variants, plus monolingual, bilingual, and multilingual BERT models.
- **Two evaluation methods**: Surprisal score accuracy (via `minicons`) and prompted multiple-choice accuracy.

## Key Findings

**Experiment 1 — Mamba vs. Transformer (English)**
- Under surprisal score evaluation, `falcon-mamba-7b-instruct` achieved the highest accuracy (0.44), outperforming all transformer baselines.
- Under prompt evaluation, Mamba models only matched transformer models trained on similar data, not all transformers (`Mistral-7B-Instruct` reached 0.57).
- Conclusion: Mamba models are competitive with, but do not consistently surpass, transformer LLMs on this task.

**Experiment 2 — Multilingual vs. Monolingual BERT (English & Chinese)**
- On English data, bilingual and multilingual BERTs performed similarly to monolingual BERT (~0.29–0.32).
- On Chinese data, monolingual `bert-base-chinese` (0.28) significantly outperformed the bilingual model (0.10 — below chance).
- Conclusion: Multilingual models do not generalize equally across languages; performance gap is especially pronounced for Mandarin Chinese.

## Models Used

| Model | Type |
|---|---|
| `tiiuae/falcon-7b`, `falcon-7b-instruct` | Transformer |
| `tiiuae/falcon-mamba-7b`, `falcon-mamba-7b-instruct` | Mamba (attention-free) |
| `mistralai/Mistral-7B-v0.3`, `Mistral-7B-Instruct-v0.3` | Transformer |
| `bert-base-uncased` | Monolingual English BERT |
| `bert-base-chinese` | Monolingual Chinese BERT |
| `Abdaoui/bert-base-en-zh-cased` | Bilingual BERT |
| `bert-base-multilingual-uncased` | Multilingual BERT |

## Datasets

- **English**: LNC dataset from Rambelli et al. (2024) — 668 lexicalized English noun-noun compounds with 9 Hatcher-Bourque relations
- **Chinese**: Self-created dataset (`chinese_LNC_with_incorrect_num.json`) — 176 Mandarin Chinese compounds sourced from Ji & Gagné (2007), manually annotated with Hatcher-Bourque relations and custom Chinese paraphrase templates

## Usage

**Analyze surprisal score results:**
```bash
python data_analysis.py --mode surprisal --csv_files your_model_scores.csv
```

**Analyze prompt choice results (supports multiple files for batched outputs):**
```bash
python data_analysis.py --mode prompt --csv_files file1.csv file2.csv
```

**Convert annotated CSV to JSON dataset:**
```bash
python data_converter.py --mode convert --input annotation.csv --output dataset.json
```

**Split dataset into dev and test sets:**
```bash
python data_converter.py --mode split --input dataset.json --output dev.json --output_test test.json
```

## Tools & Libraries

- [`minicons`](https://github.com/kanishkamisra/minicons) — surprisal score extraction
- HuggingFace `transformers` — model loading and text generation pipelines
- Google Colab — compute environment
## Results

Detailed outputs for each model and evaluation method are available in the `/results` directory.

## References

- Rambelli et al. (2024). *Can Large Language Models Interpret Noun-Noun Compounds?* ACL 2024.
- Gu & Dao (2023). *Mamba: Linear-time sequence modeling with selective state spaces.*
- Pepper (2022). *Hatcher-Bourque: Towards a Reusable Classification of Semantic Relations.*
- Ji & Gagné (2007). *Lexical and relational influences on the processing of Chinese modifier-noun compounds.*
