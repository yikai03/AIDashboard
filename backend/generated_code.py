import pandas as pd
import matplotlib.pyplot as plt

order_details_df = pd.read_csv("C:\\Users\\Tomta\\Desktop\\AIDashboard_2\\AIDashboard\\backend\\TrainingTable\\OrderDetails.csv")

# Calculate total sales per order
order_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']

# Group by order date and sum total sales
total_sales_by_date = order_details_df.groupby('OrderID')['TotalSales'].sum().reset_index()

# Merge with Orders.csv to get order dates
orders_df = pd.read_csv("C:\\Users\\Tomta\\Desktop\\AIDashboard_2\\AIDashboard\\backend\\TrainingTable\\Orders.csv")
merged_df = pd.merge(total_sales_by_date, orders_df, on='OrderID')

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(merged_df['OrderDate'], merged_df['TotalSales'], color='skyblue')
plt.xlabel('Order Date')
plt.ylabel('Total Sales')
plt.title('Total Sales by Order Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('chart.png')