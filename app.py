import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="CORD-19 Data Explorer", page_icon="🧬", layout="wide")

st.title("🧬 CORD-19 COVID-19 Research Data Explorer")
st.write("Explore global COVID-19 research trends using the CORD-19 metadata dataset.")


# Load data (prefer sample for fast iteration)
@st.cache_data
def load_data():
    from pathlib import Path
    candidates = [
        Path('metadata_sample.csv'),
        Path('metadata.csv'),
        Path('data') / 'metadata.csv',
    ]
    for p in candidates:
        if p.exists():
            path = p
            break
    else:
        raise FileNotFoundError(f"Could not find metadata file. Tried: {[str(p) for p in candidates]}")

    # Read only needed columns to save memory
    usecols = None
    try:
        # try to read a small header first to infer columns
        import csv
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            reader = csv.reader(fh)
            header = next(reader)
        # pick sensible subset if available
        wanted = ['title', 'abstract', 'publish_time', 'journal', 'source_x']
        usecols = [c for c in wanted if c in header]
    except Exception:
        usecols = None

    df = pd.read_csv(path, usecols=usecols, low_memory=False)

    # Basic cleaning
    if 'title' in df.columns:
        df = df.dropna(subset=['title'])
    if 'publish_time' in df.columns:
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['year'] = df['publish_time'].dt.year

    return df


df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
min_year = int(df['year'].min()) if not df['year'].isna().all() else 2019
max_year = int(df['year'].max()) if not df['year'].isna().all() else 2022
year_range = st.sidebar.slider("Select Year Range:", min_year, max_year, (min_year, max_year))

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"### Showing {len(filtered_df)} papers from {year_range[0]} to {year_range[1]}")

# Visualization 1: Publications over time
st.subheader("📈 Publications Over Time")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values, color="skyblue")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Publications")
ax.set_title("Publications by Year")
st.pyplot(fig)

# Visualization 2: Top Journals
st.subheader("🏛️ Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, palette="coolwarm", ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Journal")
ax.set_title("Top 10 Journals Publishing COVID-19 Research")
st.pyplot(fig)

# Visualization 3: Word Cloud
st.subheader("🗣️ Frequent Words in Titles")
text = " ".join(filtered_df['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Display sample data
st.subheader("📄 Sample Data")
st.dataframe(filtered_df.head(10))
