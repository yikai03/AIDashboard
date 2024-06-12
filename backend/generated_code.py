import pandas as pd
import matplotlib.pyplot as plt

order_details_df = pd.read_csv("C:\\Users\\Tomta\\Desktop\\AIDashboard_2\\AIDashboard\\backend\\TrainingTable\\OrderDetails.csv")

# Calculate total sales per product
order_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']
product_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()

# Create the pie chart
plt.figure(figsize=(8, 8))
plt.pie(product_sales['TotalSales'], labels=product_sales['ProductID'].astype(str), autopct='%1.1f%%', startangle=90)
plt.title('Total Sales by Product')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig('chart.png')