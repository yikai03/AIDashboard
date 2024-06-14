import pandas as pd
import matplotlib.pyplot as plt

order_details_df = pd.read_csv("C:\\Users\\Tomta\\Desktop\\AIDashboard_2\\AIDashboard\\backend\\TrainingTable\\OrderDetails.csv")
order_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']

total_sales_by_orderdate = order_details_df.groupby('OrderDate')['TotalSales'].sum().reset_index(name='Total Sales')

plt.figure(figsize=(10, 6))
plt.bar(total_sales_by_orderdate['OrderDate'], total_sales_by_orderdate['Total Sales'], color='skyblue')
plt.xlabel('Order Date')
plt.ylabel('Total Sales')
plt.title('Total Sales by Order Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('chart.png')