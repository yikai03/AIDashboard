import pandas as pd
import matplotlib.pyplot as plt

orders_df = pd.read_csv("C:\\Users\\Tomta\\Desktop\\AIDashboard\\aidashboard\\backend\\TableStorage\\Orders.csv")

# Calculate the total order amount for each customer
customer_orders = orders_df.groupby('CustomerID')['TotalAmount'].sum().reset_index(name='Total Order Amount')

# Plot the total order amounts
plt.figure(figsize=(10, 6))
plt.bar(customer_orders['CustomerID'], customer_orders['Total Order Amount'], color='lightcoral')
plt.xlabel('Customer ID')
plt.ylabel('Total Order Amount')
plt.title('Total Order Amount by Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('chart.png')