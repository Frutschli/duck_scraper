from excel_manager import ExcelManager
from web_searcher import WebSearcher
from deepseek import DeepseekManager
from cache_manager import CacheManager
from website_manager import WebsiteManager

def main():


    # Initialize modules
    excel = ExcelManager
    web_searcher = WebSearcher
    cache = CacheManager
    website = WebsiteManager
    deepseek = DeepseekManager

    excel_path = "VME_Mitgliederverzeichnis_verdichtet_20230126.xlsx"
    company_names = excel.extract_company_names(excel_path)


    for name in company_names[:1]:
        # Store the company name in cache
        cache_data = {"company_name": name}
        cache.update_company(name, cache_data)
        print(name)
        
        # search northdata
        search_result_nd = web_searcher.search_company_northadata(name, max_results=3)
        if search_result_nd:
            searching_for = "Northdata Website" 
            success, result_url = deepseek.find_website(search_result_nd, name, searching_for)
        if success:

            current_data = cache.get_company(name) or {}
            if "urls" not in current_data:
              current_data["urls"] = []
            current_data["urls"].append(result_url)
            cache.update_company(name, current_data)

            #excel.add_to_table(excel_path, name, result_url)

            nortdata_data = website.scrape_website_morthdata(result_url)

            if nortdata_data:
                searching_for = "Charts Data"
                result  = deepseek.analyse_website(nortdata_data, name, searching_for)
                restricted_content = result["restricted_data"] 
                content = result["general_content"]

#                print(content)
                print("restricted:")
                print(restricted_content)

                current_data = cache.get_company(name) or {}
                current_data["northdata_data"] = content
                cache.update_company(name, current_data)

                for restricted_info in restricted_content.splitlines():
                    search_result_restr = web_searcher.search_company_restriceddata(name, restricted_info, max_results=3)
                    if search_result_restr:
                        searching_for = restricted_info
                        success, result_url = deepseek.find_website(search_result_restr, name, searching_for)
                    if success:
                        
                        current_data = cache.get_company(name) or {}
                        if "urls" not in current_data:
                          current_data["urls"] = []
                        current_data["urls"].append(result_url)
                        cache.update_company(name, current_data)
                        
            



        elif success == False:
            print("no url matched") 
        
        
#        # search umsatz
#        search_result_umsatz = web_searcher.search_company_restriceddata(name, max_results=3)
#        print("umsatz website")
#        if search_result_umsatz: 
#            searching_for = "Company Umsatz"
#            success, result_url = deepseek.find_website(search_result_nd, name, searching_for)
#        if success:
#            print("url_found")
#            current_data = cache.get_company(name) or {}
#            current_data["umsatz_website_url"] = result_url
#            cache.update_company(name, current_data)
#        elif success == False:
#            print("no url matched") 

#            ### NOW GOTO WEBSITE AND SEARCH FOR USEFULL INFORMATION ###

if __name__ == "__main__":
    main()