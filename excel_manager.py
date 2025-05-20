import pandas as pd

class ExcelManager:
    def extract_company_names(excel_path):
        df = pd.read_excel(excel_path)
        if "FirmenName" not in df.columns:
            raise ValueError("Die Spalte 'FirmenName' fehlt in der Excel-Datei.")
        
        names = df["FirmenName"].fillna('').tolist()
        return names

    def extract_company_name_place(excel_path, company_name):
        df = pd.read_excel(excel_path)

        if "FirmenName1" not in df.columns or "FirmenName2" not in df.columns:
            raise ValueError("Die Spalten 'FirmenName1' und/oder 'FirmenName2' fehlen in der Excel-Datei.")

        # Kombinierte Firmennamen erzeugen
        combined_names = (df["FirmenName1"].fillna('') + " " + df["FirmenName2"].fillna('')).str.strip()

        return combined_names.tolist()
    
    def add_to_table(excel_path, firmenname, northdata_website):
        df = pd.read_excel(excel_path)  

        # Spalte erstellen, falls sie nicht existiert (Achtung auf Schreibweise!)
        if "Northdata Website" not in df.columns:
            df["Northdata Website"] = ""    

        # Passende Zeilen finden (exakte Übereinstimmung)
        match = df["FirmenName"] == firmenname  

        if match.any():
            df.loc[match, "Northdata Website"] = northdata_website
            print ("Added " + northdata_website)
        else:
            print(f"Kein Eintrag mit FirmenName = '{firmenname}' gefunden.")    

        # Tabelle speichern
        df.to_excel(excel_path, index=False)