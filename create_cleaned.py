"""
Create a cleaned CSV from metadata_sample.csv (or metadata.csv fallback) and save to metadata_cleaned.csv
"""
from pathlib import Path
import pandas as pd

# Locate sample or original
candidates = [
    Path('metadata_sample.csv'),
    Path.cwd() / 'metadata_sample.csv',
    Path.cwd().parent / 'metadata_sample.csv',
    Path('metadata.csv'),
    Path.cwd() / 'data' / 'metadata.csv',
    Path.cwd().parent / 'metadata.csv',
]
for p in candidates:
    if p.exists():
        source = p
        break
else:
    raise FileNotFoundError(f"No metadata sample or original found. Tried: {candidates}")

print('Using source:', source)
# Read (for safety read only first 100k rows if original large)
df = pd.read_csv(source, low_memory=False)

# Cleaning steps
if 'publish_time' in df.columns:
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
else:
    df['publish_time'] = pd.NaT
    df['year'] = pd.NA

if 'title' in df.columns:
    df = df.dropna(subset=['title'])
else:
    df['title'] = ''

df['title_word_count'] = df['title'].astype(str).str.split().str.len()
if 'abstract' in df.columns:
    df['abstract_word_count'] = df['abstract'].fillna('').astype(str).str.split().str.len()
else:
    df['abstract_word_count'] = 0

is_preprint = None
if 'source_x' in df.columns:
    is_preprint = df['source_x'].astype(str).str.contains('preprint', case=False, na=False)
if is_preprint is None and 'arxiv_id' in df.columns:
    is_preprint = df['arxiv_id'].notna()
if is_preprint is None:
    is_preprint = pd.Series([False]*len(df), index=df.index)

df['is_preprint'] = is_preprint

if 's2_id' in df.columns:
    df = df.drop_duplicates(subset=['s2_id'])

dup_keys = [c for c in ['title','doi'] if c in df.columns]
if dup_keys:
    df = df.drop_duplicates(subset=dup_keys)
else:
    df = df.drop_duplicates(subset=['title'])

if 'journal' in df.columns:
    df['journal'] = df['journal'].fillna('Unknown')
if 'source_x' in df.columns:
    df['source_x'] = df['source_x'].fillna('Unknown')

out = Path.cwd() / 'metadata_cleaned.csv'
try:
    df.to_csv(out, index=False)
    print('Saved cleaned CSV to', out)
except Exception as e:
    out2 = Path.cwd().parent / 'metadata_cleaned.csv'
    df.to_csv(out2, index=False)
    print('Saved cleaned CSV to', out2)

print('Done. Cleaned shape:', df.shape)
