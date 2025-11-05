# CORD-19 Frameworks Assignment (Simplified)

This repository contains a small analysis of the CORD-19 metadata file and a simple Streamlit app for exploration. The project is organized to work with a smaller sample (`metadata_sample.csv`) for fast iteration and can fall back to the full `metadata.csv` if present.

## Files of interest

- `analysis.ipynb` — Jupyter notebook with Part 1–3 analysis and cleaning steps. A top markdown cell explains where files live and how to switch between sample/full.
- `app.py` — Streamlit app (basic) that loads the sample/full dataset and provides interactive charts.
- `smoke_test.py` — Quick smoke test at the repository root that ensures the sample can be loaded and that `metadata_cleaned.csv` can be written.
- `part3_export.py` — Headless exporter at the repository root for Part 3 visualizations (writes PNGs/CSVs to `outputs/`).
- `create_sample.py` — Helper to create a 50k-row `metadata_sample.csv` from the full `metadata.csv` if present.
- `create_cleaned.py` — Script implementing the cleaning pipeline and writing `metadata_cleaned.csv`.
- `metadata_sample.csv` — (optional) sample dataset used for development (50k rows by default).
- `metadata_cleaned.csv` — cleaned dataset produced by the notebook or scripts.
- `outputs/` — generated PNG and CSV outputs from Part 3.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv venv
# Activate
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the smoke test (verifies sample loads and cleaned CSV is written):

```powershell
python smoke_test.py
```

4. Run the Streamlit app (opens a local browser):

```powershell
streamlit run app.py
```

5. Reproduce Part 3 exports (headless):

```powershell
python part3_export.py
# outputs will be written to the outputs/ folder
```
Replace the commands above with the root-level scripts when running locally:

```powershell
python smoke_test.py
python part3_export.py
# outputs will be written to the outputs/ folder
```

Notes:
 - If `metadata_sample.csv` is missing and you have the full `metadata.csv` (large), `smoke_test.py` and the notebook will attempt to create a 50k-row `metadata_sample.csv` for you.
 - If you plan to run in CI, the included workflow will run `smoke_test.py` only when `metadata_sample.csv` or `metadata.csv` is present.

If you'd like, I can also add an example results report (`REPORT.md`) summarizing the notebook outputs.
# Frameworks_Assignment - CORD-19 Data Explorer

## Overview
This project explores the CORD-19 research dataset using Python frameworks — pandas, matplotlib, seaborn, and Streamlit — to visualize global COVID-19 research trends.

## Learning Objectives
- Load and clean real-world data using pandas
- Perform exploratory data analysis (EDA)
- Create visualizations for trends and insights
- Build an interactive Streamlit web app

## Results (expected)
- Publications increased sharply in 2020.
- Preprints and repositories like medRxiv/bioRxiv appear among top sources.
- Common words in titles include "COVID", "SARS-CoV-2", and "health".

## How to Run

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Run the Streamlit app:

```powershell
streamlit run app.py
```

## Notes
- Place the `metadata.csv` file in the `data/` folder before running.
- For large datasets, consider working with a sampled CSV while developing.

## Reflection
This project helps practice the data science workflow: load, clean, explore, visualize, and share results interactively using Streamlit.
