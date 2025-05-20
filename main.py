from excel_manager import ExcelManager
from web_searcher import WebSearcher
from llm_processor.ollama_client import analyse_website_text

def main():

    # Initialize modules
    excel = ExcelManager
    web_searcher = WebSearcher

    excel_path = "VME_Mitgliederverzeichnis_verdichtet_20230126.xlsx"
    company_names = excel.extract_company_names(excel_path)


    for name in company_names[:1]: 
        search_result = web_searcher.search_company_names(name)
        if search_result: 
            is_website = analyse_website_text(search_result, name)   
            if True: 
                excel.add_to_table(excel_path, name, search_result.get('href', ''))
            elif False:
                print("isnt Website")
            


if __name__ == "__main__":
    main()