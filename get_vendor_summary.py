import sqlite3
import pandas as pd
import logging
import os
import numpy as np
from sqlalchemy import create_engine

# # Import the ingest_db function from your first script!
# from ingestion_db import ingest_csv_to_db as ingest_db

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure Logging
logging.basicConfig(
    filename='logs/get_vendor_summary.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def create_vendor_summary(conn):
    """Executes heavy SQL joins to create the summarized table."""
    logging.info("Creating vendor summary table via SQL...")
    
    query = """
    WITH FreightSummary AS (
        SELECT VendorNumber, SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT 
            p.VendorNumber, 
            p.VendorName, 
            p.Brand, 
            p.Description,
            pp.Price AS ActualPrice, 
            p.PurchasePrice, 
            SUM(p.Quantity) AS TotalPurchaseQuantity, 
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        LEFT JOIN purchase_prices pp ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description
    ),
    SalesSummary AS (
        SELECT 
            VendorNo AS VendorNumber,  -- FIXED: Aliased VendorNo to match the other tables
            Brand, 
            SUM(SalesQuantity) AS TotalSalesQuantity, 
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand       -- FIXED: Grouping by the actual column name
    )
    SELECT 
        ps.VendorNumber, 
        ps.VendorName, 
        ps.Brand, 
        ps.Description,
        ps.PurchasePrice, 
        ps.ActualPrice, 
        ss.TotalSalesQuantity, 
        ss.TotalSalesDollars, 
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        ps.TotalPurchaseQuantity, 
        ps.TotalPurchaseDollars, 
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss ON ps.VendorNumber = ss.VendorNumber AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs ON ps.VendorNumber = fs.VendorNumber;
    """

    df = pd.read_sql_query(query, conn)
    return df

def clean_data(df):
    """Cleans the aggregated data and adds calculated business features."""
    logging.info("Cleaning data and adding new calculated features...")
    
    # 1. Fill missing values with 0
    df.fillna(0, inplace=True)
    
    # 2. Remove irrelevant white spaces from Vendor names
    df['VendorName'] = df['VendorName'].str.strip()
    
    # 3. Create new KPIs
    df['Gross_Profit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    
    df['Profit_Margin'] = np.where(df['TotalSalesDollars'] > 0, 
                                   (df['Gross_Profit'] / df['TotalSalesDollars']) * 100, 0)
    
    df['Stock_Turnover'] = np.where(df['TotalPurchaseQuantity'] > 0,
                                    df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'], 0)
    
    df['Sales_to_Purchase_Ratio'] = np.where(df['TotalPurchaseDollars'] > 0,
                                             df['TotalSalesDollars'] / df['TotalPurchaseDollars'], 0)
    
    return df

if __name__ == "__main__":
    logging.info("Starting vendor summary process...")
    
    # Database Connections
    db_path = 'inventory.db'
    conn = sqlite3.connect(db_path)
    engine = create_engine(f'sqlite:///{db_path}')
    
    try:
        # Step 1: Create vendor summary using SQL
        summary_df = create_vendor_summary(conn)
        logging.info("Top 5 records after SQL creation fetched.")
        
        # Step 2: Clean data and calculate metrics
        cleaned_df = clean_data(summary_df)
        logging.info("Data cleaned successfully.")
        
        # Step 3: Ingest back to database (The Fix is right here!)
        logging.info("Ingesting 'vendor_sales_summary' back into database...")
        cleaned_df.to_sql('vendor_sales_summary', con=engine, if_exists='replace', index=False)
        
        logging.info("Ingestion complete. vendor_sales_summary table created.")
        print("Successfully created vendor_sales_summary table in the database!")
        
    except Exception as e:
        logging.error(f"Error during execution: {e}")
        print(f"An error occurred: {e}")
        
    finally:
        conn.close()