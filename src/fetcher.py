from duckduckgo_search import DDGS

def get_search_urls(query, num_results):
    urls = []
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=num_results)
        for result in results:
            urls.append(result["href"])
    return urls
