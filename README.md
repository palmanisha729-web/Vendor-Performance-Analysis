# Vendor Performance & Inventory Optimization Analysis 📊
## 📌 Project Overview
This project evaluates vendor performance, pricing strategies, and inventory health to identify opportunities for profit maximization and cost reduction. By analyzing over 10,000+ transactional records across multiple fragmented tables, this end-to-end data pipeline uncovers inefficiencies—such as **$2.71M** locked in unsold inventory—and provides data-driven recommendations to optimize capital allocation and marketing budgets.

## 🏗️ Data Architecture & Workflow
The project follows a robust ETL (Extract, Transform, Load) and analytical pipeline:
1. **Data Centralization (SQLite):** Ingested raw datasets (Sales, Purchases, Vendor Invoices, Prices) into a localized `inventory.db` relational database.
2. **Data Aggregation (Advanced SQL):** Engineered a heavy data extraction script (`get_vendor_summary.py`) utilizing **Common Table Expressions (CTEs)** and complex `LEFT JOIN`s to aggregate multi-level data into a single "Source of Truth" table.
3. **Data Cleaning & EDA (Python/Pandas):** Handled missing values, standardized text, and engineered critical business KPIs (Gross Profit, Profit Margin, Stock Turnover) using vectorized operations in Jupyter Notebooks. Conducted statistical hypothesis testing using `SciPy`.
4. **Business Intelligence (Power BI & DAX):** Exported cleaned data structures via `export.py` to design an interactive dashboard. Utilized DAX to create dynamic measures for deeper granularity and outlier detection.

## 📂 Repository Structure
* `get_vendor_summary.py`: Executes heavy SQL joins and creates the aggregated database table.
* `vendor_performance_analysis.ipynb`: Comprehensive Exploratory Data Analysis (EDA), statistical testing, and visualization using Seaborn/Matplotlib.
* `export.py`: Automates the extraction of Pandas DataFrames into physical `.csv` files for BI tool integration.
* `Vendor_Dashboard.pbix`: The final interactive Power BI dashboard.

## 💡 Key Findings & Insights
* **The "Profitability Paradox":** Hypothesis testing revealed that low-volume vendors maintain significantly higher profit margins (**40.48% - 42.62%**) compared to high-volume top-performing vendors (**30.74% - 31.61%**).
* **Capital Allocation Risk:** An estimated **$2.71M** is tied up in unsold inventory, driven largely by obsolete stock with zero sales quantities.
* **Bulk Pricing Dynamics:** Vendors purchasing in bulk achieve a **~72% reduction** in unit cost ($10.78 per unit). However, faster stock turnover showed a weak negative correlation (-0.055) with profit margin, indicating that moving inventory faster does not automatically translate to higher profitability.
* **Operational Anomalies:** Identified severe freight cost inefficiencies (variance up to $257K) and loss-making transactions heavily discounting below purchase costs.

## 🚀 Strategic Recommendations
1. **Reallocate Marketing:** Redirect advertising budgets toward the identified low-volume, high-margin "Target Brands" to yield disproportionately higher gross profits.
2. **Liquidate Dead Stock:** Implement aggressive bundling or targeted discount campaigns for the specific products contributing to the $2.71M in locked capital.
3. **Audit Logistics & Pricing:** Investigate logistics contracts causing freight spikes and review algorithmic pricing to prevent sub-cost liquidations.

## 📈 Dashboard Preview
<img width="1168" height="783" alt="Screenshot 2026-02-16 184757" src="https://github.com/user-attachments/assets/098d7b05-2792-4330-af73-c91d1d8b1940" />



## 👨‍💻 Author
**Manisha Pal**
* Pursuing BS in Data Science and Programming, IIT Madras
* [Connect with me on LinkedIn](www.linkedin.com/in/manisha-pal-a52250258)
