from excel_manager import ExcelManager
from web_searcher import WebSearcher
from llm_processor.ollama_client import analyse_website_text
from deepseek import deepseek_chat
from cache_manager import CacheManager

def main():

    # Initialize modules
    excel = ExcelManager
    web_searcher = WebSearcher
    cache = CacheManager

    excel_path = "VME_Mitgliederverzeichnis_verdichtet_20230126.xlsx"
    company_names = excel.extract_company_names(excel_path)


    for name in company_names[:1]: 
        cache.clear_cache()
        cache_data = cache.get_company(name)
        cache.update_company(name, cache_data)

        # search northdata
        search_result_nd = web_searcher.search_company_northadata(name, max_results=3)
        print("northdata website")
        if search_result_nd:
            searching_for = "Northdata Website" 
            success, result_url = deepseek_chat(search_result_nd, name, searching_for)
        if success:
            print("url_found")
            current_data = cache.get_company(name) or {}
            current_data["northdata_url"] = result_url
            cache.update_company(name, current_data)

            ### NOW GOTO WEBSITE AND SEARCH FOR USEFULL INFORMATION ###

        elif success == False:
            print("no url matched") 
        
        
        # search umsatz
        search_result_umsatz = web_searcher.search_company_umsatz(name, max_results=3)
        print("umsatz website")
        if search_result_umsatz: 
            searching_for = "Company Umsatz"
            success, result_url = deepseek_chat(search_result_nd, name, searching_for)
        if success:
            print("url_found")
            current_data = cache.get_company(name) or {}
            current_data["umsatz_website_url"] = result_url
            cache.update_company(name, current_data)
        elif success == False:
            print("no url matched") 

            ### NOW GOTO WEBSITE AND SEARCH FOR USEFULL INFORMATION ###

if __name__ == "__main__":
    main()