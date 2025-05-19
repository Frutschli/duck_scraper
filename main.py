
from excel_exporter import ExcelExporter
from duckduck import DuckDuckSearch
from llm_processor.ollma_client import OllamaClient

def main():
    search = DuckDuckSearch
    ollamaClient = OllamaClient

    organisation = ExcelExporter.get_urls(1)
    print(organisation)

    try:
        search_result = search.run_search(organisation)
        print (search_result)
        ollamaClient.analyse_website_text(search_result, organisation)
    except Exception as e:
        print(f"An error ocurred: {e}")


if __name__ == "__main__":
    main()