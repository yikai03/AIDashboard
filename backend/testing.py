#Testing connection to SQL Server

import SQLConnection

# connection = SQLConnection.getTop5Data("SQL Server", "LAPTOP-AT45JF46\\NEWMSSQLSERVER", "Sales_DB", "Orders")

# print(connection)
# tableName = SQLConnection.getTableName("SQL Server", "LAPTOP-AT45JF46\\NEWMSSQLSERVER", "Sales_DB")
# print(tableName)

import pyodbc
import pandas as pd
import os
import glob

# connection = pyodbc.connect(
#     'DRIVER={SQL Server};'
#     'SERVER=LAPTOP-AT45JF46\\NEWMSSQLSERVER;'
#     'DATABASE=Sales_DB;'
#     'Trusted_Connection=yes;'
# )

# allTableName = ["Orders", "Customers", "Products", "Employees", "Shipments", "Categories", "OrderDetails", "PaymentMethods"]

# for filename in glob.glob("C:\\Users\\YC PUAH\\OneDrive - Asia Pacific University\\L2S2\\Internship\\Tomta\\AIDashboard\\backend\\TableStorage\\*.csv"):
#   os.remove(filename)

# for tableName in allTableName:
#   df = pd.read_sql(f"Select * From {tableName}", connection)

#   print(df)

#   df.to_csv(f"C:\\Users\\YC PUAH\\OneDrive - Asia Pacific University\\L2S2\\Internship\\Tomta\\AIDashboard\\backend\\TableStorage\\{tableName}.csv", index=False)

# cwd2 = os.getcwd()
# relativePath2 = "TableStorage"
# folderPath2 = os.path.join(cwd2, relativePath2)
# allFile = "*.csv"
# for filename in glob.glob(os.path.join(folderPath2, allFile)):
#     os.remove(filename)


'''
import React from "react";

function ExampleComponent() {
  const [serverName, setServerName] = React.useState("");

  const handleChange = (event) => {
    // Sanitize the input value by replacing single backslashes with double backslashes
    const sanitizedValue = event.target.value.replace("\\", "\\\\");
    setServerName(sanitizedValue);
  };

  return (
    <div>
      <label htmlFor="serverName">Server Name:</label>
      <input
        type="text"
        id="serverName"
        value={serverName}
        onChange={handleChange} // Sanitize input value onChange
      />
    </div>
  );
}
'''

#__________________________________________________________________________________________________________________________________

# import json
# filePath = "C:\\Users\\YC PUAH\\OneDrive - Asia Pacific University\\L2S2\\Internship\\Tomta\\AIDashboard\\backend\\DataStorage\\SQLConnection_New\\SQLConnection1_New.json"

# with open(filePath, 'r') as file:
#   data = json.load(file)
#   # Extract the table names from the Connection array
# table_names = [connection['Table'] for connection in data['Connection']]

# # Print the table names
# for table_name in table_names:
#     print(table_name)

# print(table_names)


# import json

# # Load the JSON data from the file
# with open('/c:/Users/YC PUAH/OneDrive - Asia Pacific University/L2S2/Internship/Tomta/AIDashboard/backend/DataStorage/SQLConnection_New/SQLConnection1_New.json') as file:
#     data = json.load(file)

# # Extract the table names from the Connection array
# table_names = [connection['Table'] for connection in data['Connection']]

# # Print the table names
# for table_name in table_names:
# print(table_name)

# import AI
import pandas as pd
import os
import pandas as pd
# AI.newChat()
# AI.getUserMessage("RbQAHQe9No", "Give me the bar chart of total orders based on different product")

# Get the current working directory
cwd = os.getcwd()

# Construct the relative path to the Orders.csv file
relative_path = "TableStorage"
relative_path2 = "*.csv"

# Combine the current working directory and the relative path
file_path = os.path.join(cwd, relative_path)
file_path2 = os.path.join(file_path, relative_path2)
# Read the Orders.csv file

print(file_path2)

# folderPath = "C:\\Users\\YC PUAH\\OneDrive - Asia Pacific University\\L2S2\\Internship\\Tomta\\AIDashboard\\backend\\TableStorage"
# files = os.listdir(folderPath)
# fileNames = [file for file in files if os.path.isfile(os.path.join(folderPath, file))]
# dataFrame = [pd.read_csv(f"{folderPath}\\{fileName}") for fileName in fileNames]

# dataTypeInDataFrame = [df.dtypes for df in dataFrame]

# print("Files::::::", files)

# print("File Names::::::", fileNames)

# print("Data Type in Data Frame::::::", dataTypeInDataFrame)














