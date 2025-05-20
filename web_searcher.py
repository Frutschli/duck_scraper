from duckduckgo_search import DDGS

class WebSearcher:
    def search_company_names(company_name):


        query = f"site:northdata.de {company_name}"
        with DDGS(proxy="tb", timeout=20) as ddgs:
            results = ddgs.text(query, max_results=1)
            for r in results:
                return r
