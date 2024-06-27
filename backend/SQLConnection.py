'''
No need to use multi thread to connect to 10 databases, that will cause a lot of problems and bad for efficiency.

one connection then use sql query to use multiple table

unless want to use multiple table in different database, then need to use multi thread to connect to multiple databases
'''

import pyodbc
import glob
import os
import pandas as pd

def getCursor(driver, server, database): # Function to get cursor
    try: 
        connection = pyodbc.connect( # Connection to SQL Server
            f'DRIVER={driver};'+
            f'Server={server};'+
            f'Database={database};'+
            'Trusted_Connection=yes'
        )
        cursor = connection.cursor() # Cursor to execute SQL queries
        return cursor # Return cursor
    except Exception as e: # Exception handling
        # print(f'Error: {e}') # Print error message
        return None # Return none
    
def connectSQL(driver, server, database): # Function to connect to SQL Server
    success = 0 # Variable to check if connection is successful
    try:
        cursor = getCursor(driver, server, database) # Get cursor
        success = 1 # Set success to 1 if cursor is not None
    except Exception as e: # Exception handling
        print(f'Error: {e}') # Print error message
        success = 0

    if (success == 1): # If connection is successful
        return "Connection Successful" # Return connection successful
    else:
        return "Connection Unsuccessful" # Return connection unsuccessful
    
def getTop5Data(Driver, Server, Database, Table): # Function to get top 5 data from table
    # driver = connection_info.get("Driver", "")
    # server = connection_info.get("Server", "")
    # database = connection_info.get("Database", "")
    # table = connection_info.get("Table", "")

    connection = pyodbc.connect( # Connection to SQL Server
    f'DRIVER={Driver};'+
    f'Server={Server};'+
    f'Database={Database};'+
    'Trusted_Connection=yes'
    )
    cursor = connection.cursor() # Cursor to execute SQL queries
    cursor.execute(f'SELECT TOP 5 * FROM {Table}') # Execute SQL query to get top 5 data from table
    data = [] # List to store data
    for row in cursor: # Loop through cursor
        data.append(row) # Append row to data list
    column_names = [column.column_name for column in cursor.columns(table=Table)] # Get column names
    return data, column_names

def getTableName(Driver, Server, Database):
    connection = pyodbc.connect(
    f'DRIVER={Driver};'+
    f'Server={Server};'+
    f'Database={Database};'+
    'Trusted_Connection=yes'
    )
    cursor = connection.cursor() # Cursor to execute SQL queries
    cursor.execute(f'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\'') # Execute SQL query to get top 5 data from table
    data = cursor.fetchall() # Fetch all data
    tableNames = [item[0] for item in data] # Get table names
    info = [Driver, Server, Database] # Store connection info
    return tableNames, info # Return table names and connection info

def storeSQLInStorage(allTableName, info): # Function to store SQL data in storage
    connection = pyodbc.connect( # Connection to SQL Server
        f'DRIVER={info[0]};'
        f'SERVER={info[1]};'
        f'DATABASE={info[2]};'
        'Trusted_Connection=yes;'
    )
    cwd2 = os.getcwd() # Get current working directory
    relativePath2 = "TableStorage" # Relative path to storage
    folderPath2 = os.path.join(cwd2, relativePath2) # Folder path to storage
    allFile = "*.csv" # File extension
    for filename in glob.glob(os.path.join(folderPath2, allFile)): # Loop through files in storage
        os.remove(filename) # Remove file

    for tableName in allTableName: # Loop through table names
      df = pd.read_sql(f"Select * From {tableName}", connection) # Read SQL data into pandas DataFrame

    #   print(df)
      df.to_csv(os.path.join(folderPath2, f"{tableName}.csv"), index=False) # Store data in storage

def storeTrainingDataset(allTableName, info): # Function to store training dataset
    connection = pyodbc.connect( # Connection to SQL Server
        f'DRIVER={info[0]};'
        f'SERVER={info[1]};'
        f'DATABASE={info[2]};'
        'Trusted_Connection=yes;'
    )
    cwd2 = os.getcwd() # Get current working directroy
    relativePath2 = "TrainingTable"  # Relative path to training table
    folderPath2 = os.path.join(cwd2, relativePath2) # Folder path to training table
    allFile = "*.csv" # File extension
    for filename in glob.glob(os.path.join(folderPath2, allFile)): # Loop through files in training table
        os.remove(filename) # Remove file

    for tableName in allTableName:  # Loop through table names
      df = pd.read_sql(f"Select * From {tableName}", connection) # Read SQL data into pandas DataFrame

    #   print(df)
      df.to_csv(os.path.join(folderPath2, f"{tableName}.csv"), index=False) # Store data in training table


