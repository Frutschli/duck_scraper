import pandas as pd

class ExcelExporter:

    @staticmethod
    def get_urls(limit=1):
        # Load the Excel file and sheet
        df = pd.read_excel("2025-05-06 - Leads List Louis.xlsx", sheet_name="Enriched Data")
        
        # Extract the specific column and limit the rows
        column_data = df["organization_name"].head(limit).tolist()
        
        # Return only the requested number of results
        return column_data
