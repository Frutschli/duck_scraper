from duckduckgo_search import DDGS

class WebSearcher:
    def search_company_northadata(company_name, max_results):
        query = f'site:northdata.de "{company_name}"'
        results_list = []
        with DDGS(proxy="tb", timeout=20) as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for r in results:
                results_list.append(r)
        return results_list
    

    def search_company_restriceddata(company_name, topic, max_results):
        topic = topic.strip()
        query = f'{company_name} "{topic}" -site:northdata.de' # +amount 
        results_list = []
        with DDGS(proxy="tb", timeout=20) as ddgs:
            results = ddgs.text(query, max_results=max_results)
            print(query)
            for r in results:
                results_list.append(r)
        return results_list
    

#    restr_l = ["Umsatz   "]
#    for restr in restr_l:  
#        results = search_company_restriceddata("BBM Einrichtungshaus GmbH", restr, max_results=7)
#        print(results)