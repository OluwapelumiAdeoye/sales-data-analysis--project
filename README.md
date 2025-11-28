Sales Data Analysis Project

A clean, end-to-end data analysis project using a synthetic sales dataset.  
The goal was to practice real-world data cleaning, feature engineering, time-series analysis, KPI generation, and visualization—using only Python and pandas.

Dataset source: https://www.opendatabay.com/data/synthetic

---

#This Project Covers

### 1. Data Cleaning
- Removed duplicates  
- Handled missing values  
- Stripped whitespace  
- Corrected data types  
- Validated column names  
- Backed up the cleaned dataset  

###2. Feature Engineering
- Gross Revenue, Discount Amount, Net Revenue, Profit  
- Extracted Month, Week, Quarter, Day of Week  
- Region + Sales Rep combined field  
- Created business metrics like Average Order Value  

###3. Time-Series Analysis
- Converted Sale_Date → datetime  
- Set DateTimeIndex for resampling  
- Daily/Weekly/Monthly revenue trends  
- 7-day & 30-day rolling averages  
- Lag features for past comparisons  

###4. Grouped KPIs
- Revenue & quantity by Product, Region, Sales Rep  
- Online vs Retail performance  
- New vs Returning customer behavior  
- Top products and most profitable categories  

### 5.Filtering & Insights
- High-value transactions  
- Large discounts & anomalies  
- Low-profit or negative-profit sales  
- Quantity spikes and patterns  

### 6. Visualizations
- Monthly revenue trends  
- Rolling averages  
- Regional performance  
- Top products  
- Discount distributions  

### 7.Final Summary Dataset
Created a final aggregated report containing:
- Total Revenue  
- Total Quantity Sold  
- Total Profit  
- Channel KPIs  
- Monthly & quarterly summaries  

Saved as: `data_summary_10.csv`

---

## 🧰 Tech Used
- Python  
- Pandas  
- NumPy  
- Matplotlib  
- Jupyter Notebook  

---

## 🚀 How to Use
```bash
git clone <your-repo-url>
pip install -r requirements.txt
jupyter notebook
📣 Connect
LinkedIn: your link
Email: your email

Dataset is fully synthetic and safe for pub
