import pandas as pd
import os
from sqlalchemy import create_engine

# SQLite DB create / connect
engine = create_engine("sqlite:///inventory.db")

# CSV folder path (current folder)
BASE_PATH = os.getcwd()

csv_files = {
    "begin_inventory": "begin_inventory.csv",
    "end_inventory": "end_inventory.csv",
    "purchases": "purchases.csv",
    "purchase_prices": "purchase_prices.csv",
    "sales": "sales.csv",
    "vendor_invoice": "vendor_invoice.csv"
}

def ingest_csv_to_db():
    for table_name, file_name in csv_files.items():
        file_path = os.path.join(BASE_PATH, file_name)
        df = pd.read_csv(file_path)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"{table_name} loaded successfully")

if __name__ == "__main__":
    ingest_csv_to_db()
