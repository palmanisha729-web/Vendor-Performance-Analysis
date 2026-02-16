import pandas as pd
import sqlite3

# 1. Database se connect karein
conn = sqlite3.connect('inventory.db')

# 2. Main table ko read karein
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary", conn)

print("Main data load ho gaya. Ab CSV files generate kar rahe hain...")

# 3. Main CSV export karein
df.to_csv('vendor_sales_summary.csv', index=False)
print(" - vendor_sales_summary.csv saved!")

# 4. Brand Performance table recreate karke export karein
brand_performance = df.groupby('Description').agg({
    'TotalSalesDollars': 'sum',
    'Profit_Margin': 'mean'
}).reset_index()
brand_performance.to_csv('BrandPerformance.csv', index=False)
print(" - BrandPerformance.csv saved!")

# 5. Purchase Contribution table recreate karke export karein
purchase_contribution = df.groupby('VendorName').agg({
    'TotalPurchaseDollars': 'sum',
    'Gross_Profit': 'sum',
    'TotalSalesDollars': 'sum'
}).reset_index()
purchase_contribution.to_csv('PurchaseContribution.csv', index=False)
print(" - PurchaseContribution.csv saved!")

# 6. Low Turnover Vendor table recreate karke export karein
low_turnover = df[df['Stock_Turnover'] < 1].groupby('VendorName')[['Stock_Turnover']].mean()
low_turnover = low_turnover.sort_values('Stock_Turnover').head(10).reset_index()
low_turnover.to_csv('LowTurnoverVendor.csv', index=False)
print(" - LowTurnoverVendor.csv saved!")

print("\nSuccess Bhai! Saari 4 CSV files aapke folder mein ban chuki hain. Ab Power BI open kar lo.")

# Connection close karein
conn.close()