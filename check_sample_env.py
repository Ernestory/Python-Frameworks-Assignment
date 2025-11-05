import sys, os
import pandas as pd
from pathlib import Path

out_path = Path('metadata_check_output.txt')
orig = Path('metadata_sample.csv')

lines = []
lines.append(f'PYTHON: {sys.executable}')
lines.append(f'PYTHON_VERSION: {sys.version.split()[0]}')
lines.append(f'PANDAS: {pd.__version__}')
lines.append(f'SAMPLE_PATH: {orig}')
lines.append(f'SAMPLE_EXISTS: {orig.exists()}')

if orig.exists():
    try:
        df = pd.read_csv(orig, low_memory=False, nrows=5)
        lines.append(f'SHAPE (sample rows read): {df.shape}')
        cols = list(df.columns)
        lines.append('COLUMNS: ' + ', '.join(cols[:50]))
        lines.append('\n--- SAMPLE PREVIEW (first 3 rows) ---')
        lines.append(df.head(3).to_string())
    except Exception as e:
        lines.append('ERROR READING SAMPLE: ' + repr(e))

out_path.write_text('\n'.join(lines), encoding='utf-8')
print('WROTE:', out_path)
