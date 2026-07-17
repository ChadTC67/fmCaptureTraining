# fmCaptureTraining

Python tools for capturing Dofus/Forgemagie item stat data from the screen and training a rune prediction model from processed capture files.

The repository is intentionally Python-only. Generated screenshots, local counters, and trained pickle artifacts are ignored so the public repo stays focused on source code and reusable training data.

## What is included

- `fm_capture_training.py` listens for mouse releases, captures configured screen regions, OCRs item stats/min/max values, and writes structured JSON samples to `output_data/`.
- `train.py` trains a `RandomForestClassifier` from `fmData/preprocessedData/processed_*.json`.
- `capture_functions.py`, `ocr_functions.py`, `extraction_functions.py`, and `grid_calculation.py` contain the screen capture, OCR parsing, and rune matching helpers.
- `rune_data.py` contains rune IDs, characteristic IDs, and rune weights.
- `fmData/` contains the checked-in training dataset.

## Requirements

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- The Python packages in `requirements.txt`

Install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Install Tesseract separately. On macOS with Homebrew:

```bash
brew install tesseract
```

If Tesseract is not on your `PATH`, set `TESSERACT_CMD` before running capture:

```bash
export TESSERACT_CMD="/path/to/tesseract"
```

## Train a model

```bash
python train.py
```

By default this reads `fmData/preprocessedData` and writes:

- `model.pkl`
- `scaler.pkl`

Both files are generated artifacts and are ignored by Git. You can choose different paths:

```bash
python train.py --data-dir fmData/preprocessedData --model-file model.pkl --scaler-file scaler.pkl
```

## About the accuracy goal

This project is an experiment in pushing rune prediction toward 100% accuracy from captured Forgemagie state. It does not reach that goal. On the current checked-in processed dataset, the default training run produced about 59.6% test accuracy during cleanup verification.

The failure is not just a model-choice problem. The input data does not fully describe every factor that affects the next rune outcome, and some labels come from a noisy capture pipeline:

- OCR can misread stat names, numbers, percentages, and sink values.
- Screen regions are hard-coded and must be calibrated for each resolution and game-window position.
- The dataset is small and uneven across rune classes, so some runes have very few examples.
- Several rune choices share similar visible item states, which makes them difficult or impossible to separate from the current features alone.
- The random train/test split measures performance on captured samples, not guaranteed real-game prediction accuracy.

So the repository should be read as a data-capture and model-training attempt, not a solved predictor. Better accuracy would require cleaner labels, more balanced data, stronger feature engineering, and validation against fresh captures.

## Capture new training samples

```bash
python fm_capture_training.py
```

The script listens for mouse release events. When a click lands in a configured rune or combine-button region, it captures the relevant screen areas, runs OCR, and writes JSON into `output_data/`.

Before collecting real samples, calibrate these constants in `capture_functions.py` and `grid_calculation.py` for your screen resolution and game window position:

- `ITEM_STATS_GRID_REGION`
- `COMBINE_BUTTON_REGION`
- `RUNES_PASSED_GRID_REGION`
- `calculate_grid_item()` grid coordinates

Generated files are intentionally ignored:

- `captured_grids/`
- `captured_runes/`
- `output_data/`
- `counter.txt`
- `model.pkl`
- `scaler.pkl`

## Repository notes

This project stores model artifacts as generated local files instead of committed binaries. Rebuild them with `python train.py` from the checked-in processed data.

No license file is currently included. Add one before publishing if you want others to have explicit reuse rights.
