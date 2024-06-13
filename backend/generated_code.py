import pandas as pd
import matplotlib.pyplot as plt

orders_df = pd.read_csv("C:\\Users\\Tomta\\Desktop\\AIDashboard_2\\AIDashboard\\backend\\TrainingTable\\Orders.csv")

# Group by CustomerID and sum the TotalAmount
customer_total_amount = orders_df.groupby('CustomerID')['TotalAmount'].sum().reset_index()

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(customer_total_amount['CustomerID'], customer_total_amount['TotalAmount'], color='skyblue')
plt.xlabel('Customer ID')
plt.ylabel('Total Order Amount')
plt.title('Total Order Amount by Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('chart.png')