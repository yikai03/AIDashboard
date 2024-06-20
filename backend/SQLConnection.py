# No need to use multi thread to connect to 10 databases, that will cause a lot of problems and bad for efficiency.

# one connection then use sql query to use multiple table

# unless want to use multiple table in different database, then need to use multi thread to connect to multiple databases
import pyodbc
import glob
import os
import pandas as pd

def getCursor(driver, server, database): # get the cursor for the connection to be able to perform modification with the database
    try:
        connection = pyodbc.connect( #Build the connection string
            f'DRIVER={driver};'+ 
            f'Server={server};'+
            f'Database={database};'+
            'Trusted_Connection=yes'
        )
        cursor = connection.cursor() #Get the cursor of the connection
        return cursor
    except Exception as e: #If there is an error occur, print out the error
        print(f'Error: {e}')
        return None
    
def connectSQL(driver, server, database): #Connect to the SQL server
    success = 0
    try:
        cursor = getCursor(driver, server, database) #Get the cursor
        success = 1
    except Exception as e:
        print(f'Error: {e}')
        success = 0

    if (success == 1):
        return "Connection Successful" #If the connnection is successful, return the message
    else:
        return "Connection Unsuccessful" #Else, if the connection is unsuccessful, return the failure message
    
def getTop5Data(Driver, Server, Database, Table): #Function to get the top 5 data from the table
    connection = pyodbc.connect( #Build the connection string
    f'DRIVER={Driver};'+
    f'Server={Server};'+
    f'Database={Database};'+
    'Trusted_Connection=yes'
    )
    cursor = connection.cursor() #Get the cursor of the connection
    cursor.execute(f'SELECT TOP 5 * FROM {Table}') #Execute the query to get the top 5 data from the table
    data = [] #Initiaize the data list
    for row in cursor: #Loop through the cursor to get the data
        data.append(row) #Append the row data to the data list
    column_names = [column.column_name for column in cursor.columns(table=Table)] #Get the column names of the table and store in the list
    return data, column_names

def getTableName(Driver, Server, Database): #Function to get all the table name in the database
    connection = pyodbc.connect( #Build the connection string
    f'DRIVER={Driver};'+
    f'Server={Server};'+
    f'Database={Database};'+
    'Trusted_Connection=yes'
    )
    cursor = connection.cursor() #Get the cursor of the connection
    cursor.execute(f'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\'') #Execute the query to get all the table name in the database
    data = cursor.fetchall() #Fetch all the data from the cursor
    tableNames = [item[0] for item in data] #Get the table name and store in the list
    info = [Driver, Server, Database] #Store the driver, server and database information in the list for future use
    return tableNames, info

def storeSQLInStorage(allTableName, info): #Function to store the SQL data in our local storage
    connection = pyodbc.connect( #Build the connection string
        f'DRIVER={info[0]};'
        f'SERVER={info[1]};'
        f'DATABASE={info[2]};'
        'Trusted_Connection=yes;'
    )
    cwd2 = os.getcwd() #Get the current working directory
    relativePath2 = "TableStorage" #Set the relative path to store the data
    folderPath2 = os.path.join(cwd2, relativePath2) #Join the current working directory with the relative path to get the full path
    allFile = "*.csv" #Set the file extension to csv for easy access of the data
    for filename in glob.glob(os.path.join(folderPath2, allFile)): #Loop through the folder first to get all the data in the folder
        os.remove(filename) #Remove all the data (CSV file) in the folder to initialize the folder

    for tableName in allTableName: #Loop through all the table name that we passed into this function
      df = pd.read_sql(f"Select * From {tableName}", connection) #Read the data from the table and store in the dataframe

    #   print(df)
      df.to_csv(os.path.join(folderPath2, f"{tableName}.csv"), index=False) #Store the data in the local storage with the table name as the file name

def storeTrainingDataset(allTableName, info): #Function to store the SQL data in our local storage
    connection = pyodbc.connect( #Build the connection string
        f'DRIVER={info[0]};'
        f'SERVER={info[1]};'
        f'DATABASE={info[2]};'
        'Trusted_Connection=yes;'
    )
    cwd2 = os.getcwd() #Get the current working directory
    relativePath2 = "TrainingTable" #Set the relative path to store the data into Training Table folder

    #__________________________________
    # Difference of Table Storage folder and Training Table folder
        # Table Storage folder is to store ALL table data in the database
            #Used in first page where we show all the table data in the database
        # Training Table folder is to store table data that user selected for AI to refer to 
            #Used in second page where user select the table data for AI and chat with AI
    #__________________________________

    folderPath2 = os.path.join(cwd2, relativePath2) #Join the current working directory with the relative path to get the full path
    allFile = "*.csv" #Set the file extension to csv for easy access of the data
    for filename in glob.glob(os.path.join(folderPath2, allFile)): #Loop through the folder first to get all the data in the folder
        os.remove(filename) #Remove all the data (CSV file) in the folder to initialize the folder

    for tableName in allTableName: #Loop through all the table name that we passed into this function
      df = pd.read_sql(f"Select * From {tableName}", connection) #Read the data from the table and store in the dataframe

    #   print(df) 
      df.to_csv(os.path.join(folderPath2, f"{tableName}.csv"), index=False) #Store the data in the local storage with the table name as the file name