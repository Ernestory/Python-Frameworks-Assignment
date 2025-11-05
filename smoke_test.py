"""Quick smoke test for the metadata sample + cleaned write.

Usage:
    python smoke_test.py

Exits with code 0 on success, non-zero on failure.
"""
from pathlib import Path
import sys
import pandas as pd


def find_sample():
    candidates = [
        Path('metadata_sample.csv'),
        Path.cwd() / 'metadata_sample.csv',
        Path.cwd().parent / 'metadata_sample.csv',
        Path.cwd() / 'data' / 'metadata_sample.csv',
        Path.cwd().parent / 'data' / 'metadata_sample.csv',
    ]
    for p in candidates:
        if p.exists():
            return p
    # fallback: try to find original metadata.csv and create sample
    origs = [
        Path('metadata.csv'),
        Path.cwd() / 'data' / 'metadata.csv',
        Path.cwd().parent / 'metadata.csv',
        Path.cwd().parent / 'data' / 'metadata.csv',
    ]
    for o in origs:
        if o.exists():
            print('Found original metadata.csv at', o)
            try:
                df = pd.read_csv(o, low_memory=False, nrows=50000)
                out = Path.cwd() / 'metadata_sample.csv'
                df.to_csv(out, index=False)
                print('Wrote sample to', out)
                return out
            except Exception as e:
                print('Failed to create sample from', o, '->', e)
                continue
    return None


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # minimal cleaning that mirrors the notebook
    df = df.copy()
    if 'publish_time' in df.columns:
        df['publish_time'] = pd.to_datetime(df.get('publish_time'), errors='coerce')
        df['year'] = df['publish_time'].dt.year
    if 'title' in df.columns:
        df = df.dropna(subset=['title'])
        df['title_word_count'] = df['title'].astype(str).str.split().str.len()
    if 'abstract' in df.columns:
        df['abstract_word_count'] = df['abstract'].fillna('').astype(str).str.split().str.len()
    if 'journal' in df.columns:
        df['journal'] = df['journal'].fillna('Unknown')
    if 'source_x' in df.columns:
        df['source_x'] = df['source_x'].fillna('Unknown')
    # de-dup using s2_id if present
    if 's2_id' in df.columns:
        df = df.drop_duplicates(subset=['s2_id'])
    return df


def main():
    s = find_sample()
    if s is None:
        print('No sample or metadata.csv found. Please place metadata_sample.csv or metadata.csv in the project root or data/ folder.')
        sys.exit(2)
    print('Loading sample from', s)
    try:
        df = pd.read_csv(s, low_memory=False)
    except Exception as e:
        print('Failed to read sample:', e)
        sys.exit(3)
    print('Sample shape:', df.shape)

    # run minimal cleaning and write cleaned csv
    df_clean = basic_clean(df)
    out = Path.cwd() / 'metadata_cleaned.csv'
    try:
        df_clean.to_csv(out, index=False)
        print('Wrote cleaned CSV to', out)
    except Exception as e:
        print('Failed to write cleaned CSV:', e)
        sys.exit(4)

    # basic sanity checks
    if df_clean.shape[0] == 0:
        print('Cleaned dataframe has zero rows — something is wrong')
        sys.exit(5)

    print('Smoke test passed.')
    sys.exit(0)


if __name__ == '__main__':
    main()
