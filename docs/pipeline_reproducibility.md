# Dataset Pipeline and Reproducibility

This document describes the dataset generation pipeline, file meanings, and how to reproduce each dataset artifact.

## File descriptions

- `data/processed/enriched_dataset_full.csv`
  - The full semantic-enriched dataset generated from the original source.
  - Contains `question1`, `question2`, `is_duplicate`, `semantic_label`, `label_reason`, `source_dataset`, and `split`.

- `data/processed/augmented_full_full.csv`
  - A synthetic augmentation file created from the enriched dataset.
  - Used to expand the paraphrase class via simple rule-based transformations.

- `data/processed/combined_enriched_augmented.csv`
  - The merged dataset containing both the enriched base examples and augmented paraphrase examples.
  - Suitable as a large training or benchmark corpus.

- `data/processed/gold_subset_2000.csv`
  - A randomly sampled 2,000-example subset for human annotation.
  - Includes an extra `annotation_status` field.

## Reproducible commands

Generate the enriched dataset from the source file:

```bash
python src/prepare_dataset.py --source ../DupliQuest/ques/ques_pairs.csv --output data/processed/enriched_dataset_full.csv --max-rows 404290
```

Generate the full augmented dataset from the enriched dataset:

```bash
python src/augmentation.py --input data/processed/enriched_dataset_full.csv --output data/processed/augmented_full_full.csv --max-rows 404290
```

Generate Ollama-based augmentation using your local Ollama endpoint:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=qwen3.5
python src/augmentation.py --input data/processed/enriched_dataset_full.csv --output data/processed/augmented_full_ollama.csv --mode ollama --max-rows 100
```

Combine enriched and augmented datasets:

```bash
python src/combine_datasets.py --original data/processed/enriched_dataset_full.csv --augmented data/processed/augmented_full_full.csv --output data/processed/combined_enriched_augmented.csv
```

Export a 2,000-example gold subset for annotation:

```bash
python src/export_gold_subset.py --input data/processed/combined_enriched_augmented.csv --output data/processed/gold_subset_2000.csv --size 2000
```

## Baseline evaluation

Run a simple Jaccard-based baseline:

```bash
python src/baseline.py --input data/processed/combined_enriched_augmented.csv --method jaccard
```

Evaluate on the human gold subset:

```bash
python src/baseline.py --input data/processed/combined_enriched_augmented.csv --gold data/processed/gold_subset_2000.csv --method jaccard
```

If `sentence-transformers` is installed, run an embedding-based baseline:

```bash
python src/baseline.py --input data/processed/combined_enriched_augmented.csv --method embedding
```

## Notes

- The current augmentation is rule-based and is intended as a placeholder for future LLM-driven expansion.
- The gold subset is designed for human annotation and quality measurement, not for large-scale training.
- Use the `split` field if you want to create deterministic train/validation/test partitions.
