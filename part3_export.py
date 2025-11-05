"""
Run Part 3 analysis headlessly and save PNGs/CSV to outputs/
This script prefers metadata_cleaned.csv, then metadata_sample.csv, then metadata.csv
"""
from pathlib import Path
import pandas as pd
import matplotlib
# use non-interactive backend for headless/scripted environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud

sns.set_style('whitegrid')

# locate input
candidates = [
    Path('metadata_cleaned.csv'),
    Path('metadata_sample.csv'),
    Path('metadata.csv'),
    Path('data') / 'metadata.csv',
    Path.cwd().parent / 'metadata_sample.csv',
]
for p in candidates:
    if p.exists():
        source = p
        break
else:
    raise FileNotFoundError(f'No input metadata found. Tried: {candidates}')

print('Using source:', source)

outputs = Path('outputs')
outputs.mkdir(exist_ok=True)

# read
print('Reading (may take a few seconds)...')
df = pd.read_csv(source, low_memory=False)

# ensure publish_time
if 'publish_time' in df.columns:
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['month'] = df['publish_time'].dt.to_period('M').dt.to_timestamp()
else:
    df['publish_time'] = pd.NaT
    df['year'] = pd.NA

# monthly/yearly
if df['publish_time'].notna().any():
    monthly = df.groupby('month').size().sort_index()
    yearly = df.groupby('year').size().sort_index()
    monthly_roll3 = monthly.rolling(window=3, min_periods=1).mean()

    # yearly plot
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(yearly.index.astype('int'), yearly.values, color='tab:blue')
    ax.set_title('Publications by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    plt.tight_layout()
    p = outputs / 'publications_by_year.png'
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print('Wrote', p)

    # monthly plot
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(monthly.index, monthly.values, label='Monthly', color='tab:gray', alpha=0.6)
    ax.plot(monthly_roll3.index, monthly_roll3.values, label='3-month MA', color='tab:red')
    ax.set_title('Monthly Publications (with 3-month rolling average)')
    ax.set_xlabel('Month')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    p = outputs / 'publications_monthly_roll3.png'
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print('Wrote', p)
else:
    print('No publish_time available to compute time series')

# top journals
if 'journal' in df.columns:
    top_journals = df['journal'].value_counts().head(20)
    top_journals.to_csv(outputs / 'top_journals.csv')
    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x=top_journals.values, y=top_journals.index, palette='mako', ax=ax)
    ax.set_title('Top Journals')
    plt.tight_layout()
    p = outputs / 'top_journals.png'
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print('Wrote', p)

    # cumulative for top 5
    top5 = top_journals.head(5).index.tolist()
    if df['year'].notna().any():
        pivot = (df[df['journal'].isin(top5)].groupby(['year','journal']).size().unstack(fill_value=0).sort_index())
        pivot_cum = pivot.cumsum()
        pivot_cum.to_csv(outputs / 'cumulative_top5_journals.csv')
        fig, ax = plt.subplots(figsize=(10,5))
        pivot_cum.plot(ax=ax)
        ax.set_title('Cumulative Publications by Year — Top 5 Journals')
        plt.tight_layout()
        p = outputs / 'cumulative_top5_journals.png'
        fig.savefig(p, dpi=150)
        plt.close(fig)
        print('Wrote', p)

# top sources
if 'source_x' in df.columns:
    top_sources = df['source_x'].value_counts().head(20)
    top_sources.to_csv(outputs / 'top_sources.csv')
    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x=top_sources.values, y=top_sources.index, palette='viridis', ax=ax)
    ax.set_title('Top Sources')
    plt.tight_layout()
    p = outputs / 'top_sources.png'
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print('Wrote', p)

# n-grams
stopwords = set(["the","and","of","in","to","a","for","on","with","by","is","an","from","as","that","at","are","be","this","we","or","which","it","was","have","has"]) 

def tokenize(text):
    text = re.sub(r"[^a-z0-9\s]", ' ', text.lower())
    tokens = [t for t in text.split() if t and t not in stopwords and len(t)>1]
    return tokens

all_titles = df['title'].dropna().astype(str).tolist()
uni_counter = Counter()
bi_counter = Counter()
for t in all_titles:
    toks = tokenize(t)
    uni_counter.update(toks)
    bi_counter.update([" ".join(x) for x in zip(toks, toks[1:])])

top_unigrams = uni_counter.most_common(50)
top_bigrams = bi_counter.most_common(50)

# save CSVs
import csv
with open(outputs / 'top_unigrams.csv', 'w', newline='', encoding='utf-8') as fh:
    writer = csv.writer(fh)
    writer.writerow(['unigram','count'])
    writer.writerows(top_unigrams)
with open(outputs / 'top_bigrams.csv', 'w', newline='', encoding='utf-8') as fh:
    writer = csv.writer(fh)
    writer.writerow(['bigram','count'])
    writer.writerows(top_bigrams)
print('Wrote top n-gram CSVs')

# plot top 20 unigrams and bigrams
try:
    u_words, u_counts = zip(*top_unigrams[:20])
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=list(u_counts[::-1]), y=list(u_words[::-1]), palette='rocket', ax=ax)
    ax.set_title('Top 20 Unigrams in Titles')
    plt.tight_layout()
    p = outputs / 'top_unigrams.png'
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print('Wrote', p)
except Exception:
    pass

try:
    b_words, b_counts = zip(*top_bigrams[:20])
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=list(b_counts[::-1]), y=list(b_words[::-1]), palette='mako', ax=ax)
    ax.set_title('Top 20 Bigrams in Titles')
    plt.tight_layout()
    p = outputs / 'top_bigrams.png'
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print('Wrote', p)
except Exception:
    pass

# improved word cloud
wc_stopwords = set(list(WordCloud().stopwords) + list(stopwords))
text = ' '.join(all_titles)
wordcloud = WordCloud(width=1600, height=800, background_color='white', stopwords=wc_stopwords, max_words=200).generate(text)
fig = plt.figure(figsize=(16,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
p = outputs / 'wordcloud_improved.png'
fig.savefig(p, dpi=150, bbox_inches='tight')
plt.close(fig)
print('Wrote', p)

print('Done. Outputs saved to', outputs)
