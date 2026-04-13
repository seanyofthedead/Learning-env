# Grammar of Failure

UVA MSBA capstone: **does the linguistic quality of safety incident narratives
predict whether similar incidents recur?**

This repository collects safety incident reports from six federal databases
covering 2018–2025, normalizes them into a single schema, labels recurrences
at the entity level, extracts text-quality features from the narratives, and
trains a model to test the hypothesis.

## Pipeline

```
Phase 1: acquire raw data        -> data/raw/
Phase 2A: normalize schemas      -> data/processed/normalized.parquet
Phase 2B: entity link + label    -> data/processed/reports_with_labels.parquet
Phase 2C: extract features       -> data/features/*.parquet
Phase 2D: train + evaluate       -> reports/model_results.md
```

## Data sources

| Source | Domain | Access |
|---|---|---|
| NASA ASRS | Aviation self-reports | DBOL form, scripted pagination |
| NTSB CAROL | Aviation investigations | JSON API |
| OSHA Severe Injury Reports | Workplace injuries (federal OSHA) | Direct ZIP |
| OSHA ITA 300/301 | Establishment case details | Per-year ZIPs |
| MSHA Accidents | Mine safety | Direct ZIP |
| NRC LER | Nuclear event reports | Pipe-delimited text |

## Install

```bash
pip install -e .                    # core acquisition only
pip install -e .[analysis]          # + Phase 2 normalize/labels/features/models
pip install -e .[analysis,embeddings]  # + MiniLM embeddings (heavy)
python -m spacy download en_core_web_sm  # required for analysis extra
```

## Run

```bash
# Phase 1 — acquire all sources
python -m scripts.acquire_all

# Phase 1 — acquire a single source
python -m scripts.acquire_all --source osha_sir
python -m scripts.acquire_msha

# Phase 2
python -m normalize.run_all
python -m labels.run_all --window-days 365 --match-level family
python -m features.run_all
python -m models.run_all
```

## Repo layout

See `/root/.claude/plans/concurrent-sniffing-origami.md` for the full plan
and file tree. Top-level modules: `scripts/` (Phase 1), `normalize/`,
`labels/`, `features/`, `models/` (Phase 2), `reports/` (deliverable).

## Data hygiene

Raw downloads are preserved verbatim — the acquisition step never mutates
them. Normalization runs on copies. Raw/processed/features directories
are `.gitignore`d; only `manifest.json`, `ACQUISITION_LOG.md`, and
`*_stats.md` summaries are committed, which keeps provenance in git
without needing Git LFS.
