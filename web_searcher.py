from duckduckgo_search import DDGS

class WebSearcher:
    def search_company_northadata(company_name, max_results):
        query = f"site:northdata.de {company_name}"
        results_list = []
        with DDGS(proxy="tb", timeout=20) as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                results_list.append(r)
        return results_list
    

    def search_company_umsatz(company_name, max_results):
        query = f'{company_name} "Umsatz"'
        results_list = []
        with DDGS(proxy="tb", timeout=20) as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                results_list.append(r)
        return results_list