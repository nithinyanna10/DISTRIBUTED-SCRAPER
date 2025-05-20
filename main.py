import sys
import argparse
import logging
import pandas as pd
from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent / "src"))
from scraper import scrape_url
from fetcher import get_search_urls

logging.basicConfig(filename="scraper.log", level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Parallel Web Scraper")
    parser.add_argument("--query", type=str, required=True, help="Search keyword")
    parser.add_argument("--count", type=int, default=5, help="Number of sites to scrape")
    parser.add_argument("--mode", type=str, default="title", choices=["title", "headers", "links", "text"])
    parser.add_argument("--format", type=str, default="csv", choices=["csv", "json"])
    parser.add_argument("--min_words", type=int, default=0, help="Min words for filtering text")
    parser.add_argument("--retries", type=int, default=2, help="Number of retry attempts")
    args = parser.parse_args()

    urls = get_search_urls(args.query, args.count)
    urls = list(set(urls))  # Remove duplicates

    pool_args = [(url, args.mode, args.retries, args.min_words) for url in urls]

    with Pool(processes=4) as pool:
        results = list(tqdm(pool.starmap(scrape_url, pool_args), total=len(urls)))

    results = [r for r in results if not r.get("filtered")]

    # Output
    if args.format == "csv":
        pd.DataFrame(results).to_csv("results.csv", index=False)
        print("✅ Saved to results.csv")
    else:
        pd.DataFrame(results).to_json("results.json", orient="records", indent=2)
        print("✅ Saved to results.json")

if __name__ == "__main__":
    main()
