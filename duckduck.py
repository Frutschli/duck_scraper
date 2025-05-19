from duckduckgo_search import DDGS

urls = ['test']

class DuckDuckSearch:

     def run_search(urls):
        ddgs = DDGS(proxy="tb", timeout=20)
        for url in urls:
            results = ddgs.text(url, max_results=1)
            for result in results:
                return result

