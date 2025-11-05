# Submission Report — CORD-19 Frameworks Assignment

This repository contains the deliverables for the simplified CORD-19 assignment described in `Assignment_Overview.txt`.

Summary of artifacts included
- `analysis.ipynb` — Jupyter notebook implementing Part 1–3: data loading, cleaning, and visualizations.
- `app.py` — Streamlit application showing interactive charts and a sample data table.
- `requirements.txt` — pinned Python dependencies used by the project.
- `README.md` — run instructions and notes.
- `smoke_test.py` — quick smoke test to validate sample loading and cleaned CSV writing.
- `create_sample.py` / `create_cleaned.py` — helper scripts to create a 50k sample and run the cleaning pipeline.
- `outputs/` and a set of PNG/CSV outputs produced by the Part 3 exporter (if generated locally).
- `Assignment_Overview.txt` — the assignment brief (provided by the instructor).

Status vs. Assignment checklist
- Part 1: Data Loading and Basic Exploration — Implemented in `analysis.ipynb`.
- Part 2: Data Cleaning and Preparation — Implemented in `analysis.ipynb` and `create_cleaned.py`.
- Part 3: Data Analysis and Visualization — Implemented in `analysis.ipynb` and `part3_export.py`.
- Part 4: Streamlit Application — Implemented in `app.py`.
- Part 5: Documentation and Reflection — This `REPORT.md` and `README.md` provide run instructions and a short reflection.

Notes about repository state
- This folder has been intentionally disconnected from GitHub (the `.git` metadata was removed) so the files remain local-only per your request. The remote GitHub repository (if previously created) is unchanged.
- `requirements.txt` is present and pinned. Please verify its contents locally with a text editor before running `pip install -r requirements.txt`.
- If you want the repository linked to GitHub again (with history), re-clone from GitHub or re-initialize git and add a remote.

How to run locally (Windows PowerShell)
1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the smoke test (verifies sample loading and cleaned CSV writing):

```powershell
python smoke_test.py
```

4. Run the Streamlit app:

```powershell
streamlit run app.py
```

5. Generate Part 3 outputs (headless):

```powershell
python part3_export.py
# outputs will be written to the outputs/ folder
```

Recovery and re-linking notes
- To re-link this folder to a GitHub repo with a remote URL (if you want version control again):

```powershell
git init
git remote add origin https://github.com/<your-user>/<your-repo>.git
```

Contact / next actions
- If you'd like, I can:
  - Re-initialize git and push the content to a repo you control.
  - Run the Part 3 exporter and attach the results here.
  - Clean up any temporary files or duplicate outputs.

This report confirms the repository includes the elements requested by the assignment. If you'd like me to make the repo exactly match any additional constraints in the assignment text, tell me which items to change or remove and I'll apply them.
