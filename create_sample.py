import os
from pathlib import Path
import pandas as pd

orig = Path('metadata.csv')
samp = Path('metadata_sample.csv')

if not orig.exists():
    print('Original metadata.csv not found at', orig)
    raise SystemExit(1)

try:
    print('Reading first 50,000 rows from', orig)
    df = pd.read_csv(orig, low_memory=False, nrows=50000)
    df.to_csv(samp, index=False)
    print('Created sample:', samp)
    print('Rows in sample:', df.shape[0])
except Exception as e:
    print('ERROR creating sample:', e)
    raise
