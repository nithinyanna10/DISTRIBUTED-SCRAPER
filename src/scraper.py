import requests
from bs4 import BeautifulSoup
import time
import os
import logging

def scrape_url(url, mode="title", retries=2, min_words=0):
    pid = os.getpid()
    attempt = 0

    while attempt <= retries:
        try:
            start = time.time()
            logging.info(f"[PID {pid}] Starting: {url}")
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.content, "html.parser")

            if mode == "title":
                data = soup.title.string.strip() if soup.title else "No Title"

            elif mode == "headers":
                data = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]

            elif mode == "links":
                data = [a['href'] for a in soup.find_all('a', href=True)]

            elif mode == "text":
                paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                joined = " ".join(paragraphs)
                if len(joined.split()) < min_words:
                    return {"url": url, "filtered": True}
                data = paragraphs[:5]

            else:
                data = "Unknown mode"

            end = time.time()
            logging.info(f"[PID {pid}] Finished: {url} in {round(end - start, 2)}s")
            return {"url": url, "data": data}
        except Exception as e:
            logging.error(f"[PID {pid}] Error on attempt {attempt + 1}: {url} | {e}")
            attempt += 1

    return {"url": url, "error": f"Failed after {retries} retries"}
