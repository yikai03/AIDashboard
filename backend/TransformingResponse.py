import re
import subprocess

def transformResponse(response):
    # print("response: ",response)
    pattern = r'```(?:python)?\s*(.*?)\s*```'
    code_blocks = re.findall(pattern, response, re.DOTALL)
    # print("code_blocks: ",code_blocks)
    generated_codes = "\n".join(code_blocks)

    print("generated code: ",generated_codes)
    # Step 2: Write the output to a Python file
    if generated_codes.strip():
        # print(generated_codes)
        with open("generated_code.py", "w") as file:
            file.write(generated_codes)

        # For executing the Python file using subprocess
        subprocess.run(["python", "generated_code.py"])
    else:
        print("No code was generated.")

# code="import matplotlib.pyplot as plt\nimport pandas as pd\n\n# Load the Orders.csv file into a pandas DataFrame\norders_df = pd.read_csv('C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TableStorage\\\\Orders.csv')\n\n# Group the orders by ProductID and sum the TotalAmount\nproduct_sales = orders_df.groupby(['ProductID'])['TotalAmount'].sum().reset_index()\n\n# Sort the data by the summed TotalAmount in descending order\nproduct_sales = product_sales.sort_values(by='TotalAmount', ascending=False)\n\n# Create a bar chart of the sales by product\nplt.figure(figsize=(10,6))\nplt.bar(product_sales['ProductID'], product_sales['TotalAmount'])\nplt.xlabel('Product ID')\nplt.ylabel('Sales Amount')\nplt.title('Sales By Product')\n\n# Save the chart as an image file\nplt.savefig('sales_by_product.png', dpi=300)\nplt.show()"

# code = "import matplotlib.pyplot as plt\nimport pandas as pd\n\n# Load the Orders.csv file into a pandas DataFrame\norders_df    = pd.read_csv('C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TableStorage\\\\Orders.csv')\n\n# Group the orders by ProductID and sum the TotalAmount\nproduct_sales  = orders_df.groupby(['CustomerID'])['TotalAmount'].sum().reset_index()\n\n# Sort the data by the summed TotalAmount in descending order\nproduct_sales  = product_sales.sort_values(by='TotalAmount', ascending=False)\n\n# Create a bar chart of the sales by product\nplt.figure(figsize=(10,6))\nplt.bar(product_sales['CustomerID'], product_sales['TotalAmount'])\nplt.xlabel('Product ID')\nplt.ylabel('Sales Amount')\nplt.title('Sales By Product')\n\n# Save the chart as an image file\nplt.savefig('sales_by_product.png', dpi=300)\nplt.show()"

# transformResponse(code)