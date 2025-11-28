import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(
                "sample_sales_data.csv",
                skipinitialspace=True,
                keep_default_na=True,
                na_values=["NAN", "Nan", "", " ", "N/A", "n/a", "NULL", "null", "none"]
                )

df.columns = df.columns.str.strip()
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

df_copy = df.copy()

df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])

df["Gross_Revenue"] = df["Quantity_Sold"] * df["Unit_Price"]
df["Discount_Amount"] = df["Gross_Revenue"] * df["Discount"]
df["Net_Revenue"] = df["Gross_Revenue"] - df["Discount_Amount"]
df["Profit"] = (df["Unit_Price"] - df["Unit_Cost"]) * df["Quantity_Sold"]


df["Month"] = df["Sale_Date"].dt.month
df["Week_Number"] = df["Sale_Date"].dt.isocalendar().week
df["Day_of_the_week"] = df["Sale_Date"].dt.day
df["Quarter"] = df["Sale_Date"].dt.quarter

#Setting the Date as the index
df = df.set_index("Sale_Date")

#Sorting the dataframe into a variable
df_sorted_date = df.sort_values("Sale_Date")


 

#Total Net Revenue (Daily, Weekly and Monthly)
daily_net_revenue = df_sorted_date.resample("D")["Net_Revenue"].sum()
weekly_net_revenue = df_sorted_date.resample("W")["Net_Revenue"].sum()
monthly_net_revenue = df_sorted_date.resample("MS")["Net_Revenue"].sum()



#Creating a rolling average of (7 days and 30 days respectively)
df_sorted_date["7D_rolling_avg"] = df_sorted_date["Net_Revenue"].rolling("7D").mean()
df_sorted_date["30D_rolling_avg"] = df_sorted_date["Net_Revenue"].rolling("30D").mean()




#Net Revenue 7 days ago
df_sorted_date["7_days_lag_revenue"] = df_sorted_date["Net_Revenue"].shift(7)

#Daily growth percentage
df_sorted_date["Daily_growth_%"] = (df_sorted_date["Sales_Amount"] - df_sorted_date["Sales_Amount"].shift(1)) / df_sorted_date["Sales_Amount"].shift(1) * 100

#Weekly gowth percentage
df_sorted_date["Weekly_growth_%"] = (df_sorted_date["Sales_Amount"] - df_sorted_date["Sales_Amount"].shift(7)) / df_sorted_date["Sales_Amount"].shift(7) * 100

#display and approximate to % formats
#df_sorted_date['Daily_growth_%'] = df_sorted_date["Daily_growth_%"].map("{:.2f}%".format)
#df_sorted_date["Weekly_growth_%"]= df_sorted_date["Weekly_growth_%"].map("{:.2f}%".format)


#ProductID
total_quantity_sold_id = df_sorted_date.groupby("Product_ID")["Quantity_Sold"].sum()
total_net_revenue_id = df_sorted_date.groupby("Product_ID")["Net_Revenue"].sum()
average_unit_price_id = df_sorted_date.groupby("Product_ID")["Unit_Price"].mean()

#Region
total_profit_region = df_sorted_date.groupby("Region")["Profit"].sum()
total_revenue_region = df_sorted_date.groupby("Region")["Gross_Revenue"].sum()
average_discount_region = df_sorted_date.groupby("Region")["Discount_Amount"].mean()

#Sales Rep
total_revenue_sales_rep = df_sorted_date.groupby("Sales_Rep")["Gross_Revenue"].sum()
num_txn_sales_rep = df_sorted_date.groupby("Sales_Rep")["Quantity_Sold"].count()
avg_sales_amount_sales_rep = df_sorted_date.groupby("Sales_Rep")["Sales_Amount"].mean()

#Customer Type
total_revenue_cust_type = df_sorted_date.groupby("Customer_Type")["Gross_Revenue"].sum()
avg_txn_cust_type = df_sorted_date.groupby("Customer_Type")["Quantity_Sold"].mean()
txn_count_cust_type = df_sorted_date.groupby("Customer_Type")["Quantity_Sold"].count()
sales_by_customer_type = df_sorted_date["Customer_Type"].value_counts()


#Product Category
total_revenue_prod = df_sorted_date.groupby("Product_Category")["Gross_Revenue"].sum()
total_profit_prod = df_sorted_date.groupby("Product_Category")["Profit"].sum()
avg_unit_price_prod = df_sorted_date.groupby("Product_Category")["Unit_Price"].mean()


#High value sales
high_value_threshold = df_sorted_date["Net_Revenue"].quantile(0.70)
high_value_sales = df_sorted_date["Net_Revenue"] > high_value_threshold

#Low stock/Low quantity transactions
low_value_threshold = df_sorted_date["Quantity_Sold"].quantile(0.50)
low_quantity_txn = df_sorted_date["Quantity_Sold"] < low_value_threshold

#High discount sales
high_discount_sales = df_sorted_date[df_sorted_date["Discount"] > 0.2]

#Online vs Retail Channel Performance
online_vs_retail_channel = df_sorted_date.groupby("Sales_Channel").count()
sales_by_channel = df_sorted_date["Sales_Channel"].value_counts()


#Peak & Slow Moving Products
top_prod_by_Net_Revenue = df_sorted_date.groupby("Product_Category")["Net_Revenue"].sum()
top_3_by_Net_Revenue = top_prod_by_Net_Revenue.sort_values(ascending=False).head(3)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")



#Bottom Moving Products
bottom_prods_by_sales = df_sorted_date.groupby("Product_Category")["Quantity_Sold"].count()
bottom_3_products = bottom_prods_by_sales.sort_values(ascending=True).head(3)


#Most frequent discounts applied
most_dicounts_applied = df_sorted_date.groupby("Product_Category")["Discount"].count()
top_frequent_discount = most_dicounts_applied.sort_values(ascending=False)



#Revenue by Payment method
revenue_by_payment_method = df_sorted_date.groupby("Payment_Method")["Gross_Revenue"].sum()

#Online vs Retail sales performance
online_vs_retail_sales = df_sorted_date.groupby("Payment_Method")["Sales_Amount"].sum()

#Analyze New vs Returning customers for revenue and frequency
new_customer_revenue = df_sorted_date.groupby("Customer_Type")["Gross_Revenue"].sum()
new_customer_frequency = df_sorted_date.groupby("Customer_Type").count()
print(new_customer_frequency)

#Average revenue (daily, weekly, monthly)
avg_daily_revenue = df_sorted_date.resample("D")["Gross_Revenue"].mean()
avg_weekly_revenue = df_sorted_date.resample("W")["Gross_Revenue"].mean()
avg_monthly_revenue = df_sorted_date.resample("ME")["Gross_Revenue"].mean()

#Overall average revenue
overall_daily_avg = avg_daily_revenue.mean()
overall_weekly_avg = avg_weekly_revenue.mean()
overall_monthly_avg = avg_monthly_revenue.mean()

#Revenue spikes (daily, weekly, monthly)
daily_revenue_spike = df_sorted_date["Gross_Revenue"] > 1.5 * overall_daily_avg
weekly_revenue_spike = df_sorted_date["Gross_Revenue"] > 1.5 * overall_weekly_avg
monthly_revenue_spike = df_sorted_date["Gross_Revenue"] > 1.5 * overall_monthly_avg

#Discount average (daily, weekly, monthly)
avg_daily_discount = df_sorted_date.resample("D")["Discount"].sum()
avg_weekly_discount = df_sorted_date.resample("W")["Discount"].sum()
avg_monthly_discount = df_sorted_date.resample("ME")["Discount"].sum()

#Overall average discount (daily, weekly, monthly)
overall_daily_discount = avg_daily_discount.mean()
overall_weekly_discount = avg_weekly_discount.mean()
overall_monthly_discount = avg_monthly_discount.mean()

#High discounts (daily, weekly, monthly)
daily_high_discount = avg_daily_discount > (overall_daily_discount * 1.5)
weekly_high_discount = avg_weekly_discount > (overall_weekly_discount * 1.5)
monthly_high_discount = avg_monthly_discount > (overall_monthly_discount * 1.5)



#Negative or zero profit transactions
neg_profit = df_sorted_date["Profit"] <= 0

daily_neg_profit = neg_profit.resample("D").sum()
weekly_neg_profit = neg_profit.resample("W").sum()
monthly_neg_profit = neg_profit.resample("ME").sum()



#Seaborn Visualisation
#--Line plot chart--
fig, axes = plt.subplots(2, 1, figsize=(12, 6))

sns.lineplot(x=monthly_net_revenue.index, y=monthly_net_revenue.values, ax=axes[0])
axes[0].set_title("Monthly Revenue Trend")
axes[0].set_xlabel("Month")
axes[0].set_ylabel("Monthly Net Revenue")

sns.lineplot(data=df_sorted_date, x="Sale_Date", y="7D_rolling_avg", ax=axes[1])
axes[1].set_title("7-Day Net Revenue Trend")
axes[1].set_xlabel("Sale Date")
axes[1].set_ylabel("7D Average")


plt.subplots_adjust(hspace=0.5)

import matplotlib.ticker as ticker

# Rotate x-axis labels
for ax in axes:
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(6))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
    for label in ax.get_xticklabels():
        label.set_rotation(0)
        #label.set_horizontalalignment('right')


plt.tight_layout()
plt.show()
plt.close("all")

#--End of Line plot chart --



#--Bar chart visualization (1)--
plt.figure(figsize=(10, 6))

sns.barplot(
    x=top_prod_by_Net_Revenue.index,
    y=top_prod_by_Net_Revenue.values
)

plt.title("Top Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Total Net Revenue")


import matplotlib.ticker as ticker
plt.gca().yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f'{int(x):,}')
)


ax = plt.gca()
ax.set_ylim(0, top_prod_by_Net_Revenue.max() * 1.1)   # 10% extra space for y axis
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=6))


plt.xticks(rotation=0) 
plt.tight_layout()
plt.show()

#--End of barchart visualization (1)



#--Bar chart visualization (2)
plt.figure(figsize=(10, 6))

sns.barplot(
    x=total_profit_region.index,
    y=total_profit_region.values
)

plt.title("Top profits per region")
plt.xlabel("Region")
plt.ylabel("Profit")


import matplotlib.ticker as ticker
plt.gca().yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f'{int(x):,}')
)

ax = plt.gca()
ax.set_ylim(0, total_profit_region.max() * 1.1)   # 10% extra space for y axis
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=7))

plt.xticks(rotation=0)
#plt.ticklabel_format(style='plain', axis='y')  
plt.tight_layout()
plt.show()

#--End of Bar Chart visualization (2)


#--Pie Chart Visualization (1)--

plt.figure(figsize=(8,8))

plt.pie(
        sales_by_channel.values,
        labels=sales_by_channel.index,
        autopct="%1.1f%%",
        startangle=90,
)

plt.title("Sales distribution by sales channels")
plt.show()

#--End of pie chart visualization (1) --


#Start of Pie chart visulaization (2)
plt.figure(figsize=(8,8))

plt.pie(
        sales_by_customer_type.values,
        labels=sales_by_customer_type.index,
        autopct="%1.1f%%",
        startangle=90,
)

plt.title("Sales distribution by customer type")
plt.show()

#--End of pie chart visualization (2)--


#Fill empty values with NaN
df_sorted_date.fillna(pd.NA)
df_sorted_date.to_csv("data_summary_01.csv", index=False)


