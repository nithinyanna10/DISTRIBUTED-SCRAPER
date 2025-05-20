import streamlit as st
import pandas as pd
from multiprocessing import Pool
import time
from pathlib import Path
import sys
from urllib.parse import urlparse
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# NLP & Visualization imports
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import logging
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from transformers import pipeline
from keybert import KeyBERT
from rake_nltk import Rake

# Add src/ to path and import custom modules
sys.path.append(str(Path(__file__).parent / "src"))
from scraper import scrape_url
from fetcher import get_search_urls

# Streamlit page setup
st.set_page_config(page_title="Distributed Web Scraper", layout="centered")
st.title("🔍 Distributed Web Scraper")
st.markdown("Scrape **titles, headers, links, or text** from top websites using parallel processing, then analyze results with NLP & visualization.")

# Input panel
with st.sidebar:
    st.header("🛠 Scraper Settings")
    query = st.text_input("Search Keyword", "machine learning")
    count = st.slider("Number of websites to scrape", 1, 20, 5)
    mode = st.selectbox("What to scrape", ["title", "headers", "links", "text"])
    min_words = st.number_input("Minimum words (only for text mode)", min_value=0, value=0)
    output_format = st.radio("Output format", ["CSV", "JSON"])
    run_button = st.button("🚀 Start Scraping")

# Logging
logging.basicConfig(filename="scraper.log", level=logging.INFO)

# Trigger scraping
if run_button:
    with st.spinner("🔍 Fetching URLs..."):
        urls = get_search_urls(query, count)
        urls = list(set(urls))  # Deduplicate
    st.success(f"✅ Fetched {len(urls)} unique URLs.")

    pool_args = [(url, mode, 2, min_words) for url in urls]

    with st.spinner("🧹 Scraping websites in parallel..."):
        with Pool(processes=4) as pool:
            results = pool.starmap(scrape_url, pool_args)

    results = [r for r in results if not r.get("filtered")]
    df = pd.DataFrame(results)

    if df.empty:
        st.warning("No results after filtering.")
    else:
        st.subheader("✅ Scraping Results")
        st.write(df)

        # Download option
        if output_format == "CSV":
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="results.csv", mime="text/csv")
        else:
            st.download_button("⬇️ Download JSON", df.to_json(orient="records", indent=2), file_name="results.json", mime="application/json")

        # ===== Phase 4: NLP & Visualization =====
        st.markdown("---")
        st.header("🧠 NLP & Trend Analysis")

        full_text = "\n".join(df["data"].astype(str).tolist())

        # 🔤 Summarization
        st.subheader("📝 Text Summarization")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(full_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        st.success(summary)

        # 🔑 KeyBERT keywords
        st.subheader("🔑 Keywords (KeyBERT)")
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(full_text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
        st.write([kw[0] for kw in keywords])

        

        # 🌍 Domain frequency
        st.subheader("🌍 Most Frequent Domains")
        df["domain"] = df["url"].apply(lambda x: urlparse(x).netloc)
        st.bar_chart(df["domain"].value_counts())

        # ☁️ Word Cloud
        st.subheader("☁️ Word Cloud from Scraped Text")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(full_text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
