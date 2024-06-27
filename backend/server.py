from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import SQLConnection
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import random
import GeminiAI as AI
import glob
import pandas as pd

app = FastAPI() # Create a FastAPI instance

origins = [
    "http://localhost:3000",  # Assuming your frontend app runs on localhost:3000
    "http://localhost:3000/dataintegration"
]

# Add CORSMiddleware to the application
app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allows cookies to be included in cross-origin HTTP requests
    allow_methods=["*"],  # Allows all methods (e.g., GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/") # Define a root path
def read_root(): # Define a function to be executed when the root path is accessed
    return {"Welcome to": "Gemini Version"} #Return a JSON response

global UniqueUserID # Global variable to store the UniqueUserID
UniqueUserID = "" # Initialize the UniqueUserID to an empty string

#____________________LOGIN____________________ 
class UserCredentials(BaseModel): # Define a Pydantic model to validate the request body
    username: str # Define a username field of type string
    password: str # Define a password field of type string

@app.post("/login") # Define a POST route for the /login path
async def login(user: UserCredentials): # Define a function to be executed when the /login path is accessed 
    login = False # Initialize the login status to False
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\UserCredential" # Define the relative path to the UserCredential folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the UserCredential folder
    for filename in os.listdir(folderPath): # Iterate through the files in the UserCredential folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["UserName"] == user.username and userInfo["Password"] == user.password: # Check if the username and password match
                    global UniqueUserID # Declare the UniqueUserID as a global variable
                    UniqueUserID = userInfo["UniqueUserID"] # Set the UniqueUserID to the user's UniqueUserID
                    # print("UniqueUserID: " + UniqueUserID) # Print the UniqueUserID to the console
                    login = True # Set the login status to True
                    return {"status": "success", "UniqueUserID": userInfo["UniqueUserID"]} # Return a success message with the UniqueUserID
                
    #If user not found, should:
    #1. Return a message to the user that the username or password is incorrect and require admin to register
    #2. Lead to register page
    return {"status": "failed"} # Return a failed message

#____________________DATA RETRIEVAL____________________
def findUserSQLConnectionData(): #Get User's SQL Connection Data from JSON file from UniqueUserID
    # print("UniqueUserID: " + UniqueUserID)
    #Temporary local storage of JSON file 
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    # print(userInfo)
                    return userInfo # Return the user's SQL Connection data
    return None # Return None if the user's SQL Connection data is not found

def findUserSpecificSQLConnectionData(id: str): # Get User's Specific SQL Connection Data from JSON file from UniqueUserID and ConnectionID
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    driver = str(userInfo["Driver"]) # Get the driver from the user's SQL Connection data
                    server = str(userInfo["Server"]) # Get the server from the user's SQL Connection data
                    database = str(userInfo["Database"]) # Get the database from the user's SQL Connection data
                    for connection in userInfo["Connection"]: # Iterate through the connections in the user's SQL Connection data
                        if connection["ConnectionID"] == id: # Check if the ConnectionID matches the specified ConnectionID
                            # Convert non-string values to strings
                            connection_info = { # Create a dictionary with the connection information
                                "ConnectionID": str(connection["ConnectionID"]), # Convert the ConnectionID to a string
                                "Driver": driver, # Set the driver to the driver from the user's SQL Connection data
                                "Server": server, # Set the server to the server from the user's SQL Connection data
                                "Database": database, # Set the database to the database from the user's SQL Connection data
                                "Table": str(connection["Table"]), # Convert the Table to a string 
                                "ConnectionStatus": str(connection["ConnectionStatus"]), # Convert the ConnectionStatus to a string
                                "Description": str(connection["Description"]) # Convert the Description to a string
                            }
                            return connection_info # Return the connection information 
    return None # Return None if the user's specific SQL Connection data is not found

def getUserTrainingTableData(): # Get User's Training Table Data from JSON file from UniqueUserID
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    toTrainTableArray = [] # Initialize an array to store the training table data
                    for connection in userInfo["Connection"]: # Iterate through the connections in the user's SQL Connection data
                        toTrainTable = { # Create a dictionary with the training table data
                            "Table": connection["Table"], # Set the Table to the Table from the user's SQL Connection data
                            "ToTrain" : connection["ToTrain"] # Set the ToTrain status to the ToTrain status from the user's SQL Connection data
                        }
                        toTrainTableArray.append(toTrainTable) # Append the training table data to the array
                    return toTrainTableArray # Return the training table data
    return None # Return None if the user's training table data is not found

def getUserHistoryMessageWithAI(): # Get User's History Message with AI from JSON file from UniqueUserID
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\AISessionHistory" # Define the relative path to the AISessionHistory folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the AISessionHistory folder
    for filename in os.listdir(folderPath): # Iterate through the files in the AISessionHistory folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["id"] == UniqueUserID: # Check if the id matches the global UniqueUserID
                    # print(userInfo["history"]) 
                    return userInfo["history"] # Return the history message with AI
    return None # Return None if the user's history message with AI is not found

def refreshSQLConnectionData(): # Refresh the SQL Connection Data from JSON file from UniqueUserID
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    driver = str(userInfo["Driver"]) # Get the driver from the user's SQL Connection data
                    server = str(userInfo["Server"]) # Get the server from the user's SQL Connection data
                    database = str(userInfo["Database"]) # Get the database from the user's SQL Connection data
                    return driver, server, database # Return the driver, server, and database
    return None # Return None if the user's SQL Connection data is not found

#____________________DATA STORAGE____________________ #Connection bridge to JSON file (Future in data storage)
class ConnectionInfo(BaseModel): # Define a Pydantic model to validate the request body
    Driver: str # Define a Driver field of type string
    Server: str # Define a Server field of type string 
    Database: str # Define a Database field of type string

#Generate random ID for SQL Connection
def randomID(): # Define a function to generate a random ID
    randomAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" # Define a string of random alphabets
    randomNum = "0123456789" # Define a string of random numbers
    randomID = "" # Initialize the random ID to an empty string
    for i in range(0, 3): # Iterate 3 times
        randomID += randomAlpha[random.randint(0, 51)] # Append a random alphabet to the random ID
    for i in range(0, 3): # Iterate 3 times
        randomID += randomNum[random.randint(0, 9)] # Append a random number to the random ID
    return randomID # Return the random ID

def storeAllUserSQLConnectionData(allTableNames, info): # Store all User's SQL Connection Data in JSON file
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data

                toStoreJson ={ # Create a dictionary to store the JSON data
                    "UniqueUserID": UniqueUserID, # Set the UniqueUserID to the global UniqueUserID
                    "Driver": None, # Initialize the Driver to None
                    "Server": None, # Initialize the Server to None
                    "Database": None, # Initialize the Database to None
                    "Connection": [] # Initialize the Connection to an empty array
                }         
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    toStoreJson["Driver"] = info[0] # Set the Driver to the driver from the SQL Connection data
                    toStoreJson["Server"] = info[1] # Set the Server to the server from the SQL Connection data
                    toStoreJson["Database"] = info[2] # Set the Database to the database from the SQL Connection data
                    # tableNameInFile = [connection["Table"] for connection in userInfo["Connection"]]
                    # userInfo["Connection"] = []  # Empty the userInfo["Connection"] array first
                    for name in allTableNames: # Iterate through the table names
                        toStoreConnection = { # Create a dictionary to store the connection data
                            "ConnectionID": randomID(), # Generate a random ConnectionID
                            "Table": name, # Set the Table to the table name
                            "ConnectionStatus": "Test", # Set the ConnectionStatus to "Test"
                            "Description": "", # Set the Description to an empty string
                            "ToTrain": "Yes" # Set the ToTrain status to "Yes"
                        } 
                        toStoreJson["Connection"].append(toStoreConnection) # Append the connection data to the Connection array
                        # print(toStoreConnection)
                        # print('\n\n\n final json :')
                        # print(toStoreJson)
                    with open(os.path.join(folderPath, filename), "w") as file: # Open the JSON file
                        json.dump(toStoreJson, file, indent=4) # Dump the JSON data to the file
                    break

#Add/Edit Description
def addDescription(id: str, description: str): # Add/Edit Description in JSON file
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    for i in range(0, len(userInfo["Connection"])): # Iterate through the connections in the user's SQL Connection data
                        if userInfo["Connection"][i]["ConnectionID"] == id: # Check if the ConnectionID matches the specified ConnectionID
                            userInfo["Connection"][i]["Description"] = description # Set the Description to the specified Description
                            with open(os.path.join(folderPath, filename), "w") as file: # Open the JSON file
                                json.dump(userInfo, file, indent=4) # Dump the JSON data to the file
                            break # Break the loop


class TrainTable(BaseModel): # Define a Pydantic model to validate the request body
    Table: str # Define a Table field of type string
    ToTrain: str # Define a ToTrain field of type string

def updateTrainingTableData(table: TrainTable): # Update Training Table Data in JSON file
    cwd = os.getcwd() # Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" # Define the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) # Get the full path to the SQLConnection_New folder
    for filename in os.listdir(folderPath): # Iterate through the files in the SQLConnection_New folder
        if filename.endswith(".json"): # Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: # Open the JSON file
                userInfo = json.load(file) # Load the JSON data              
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID matches the global UniqueUserID
                    for i in range(0, len(userInfo["Connection"])): # Iterate through the connections in the user's SQL Connection data
                        if userInfo["Connection"][i]["Table"] == table.Table: # Check if the Table matches the specified Table
                            userInfo["Connection"][i]["ToTrain"] = table.ToTrain # Set the ToTrain status to the specified ToTrain status
                            with open(os.path.join(folderPath, filename), "w") as file: # Open the JSON file
                                json.dump(userInfo, file, indent=4) # Dump the JSON data to the file
                            break

#____________________SQL CONNECTION____________________

#Get message to know if user successfully connect to database
@app.post("/sql-connection") # Define a POST route for the /sql-connection path
async def sqlConnection(connection_info: ConnectionInfo): # Define a function to be executed when the /sql-connection path is accessed
    # tableNames = SQLConnection.getTableName(connection_info.driver, connection_info.server, connection_info.database)
    connectionInfo = {k: v for k,v in connection_info} # Convert the connection_info to a dictionary
    # print(connectionInfo)
    tableNames, info = SQLConnection.getTableName(**connectionInfo) # Get the table names and connection information
    storeAllUserSQLConnectionData(tableNames, info) # Store all User's SQL Connection Data in JSON file
    SQLConnection.storeSQLInStorage(tableNames, info) # Store the SQL Connection Data in the SQLConnection folder

    return {"status": "success"} # Return a success message

#Get User's SQL Connection Data when user refresh the page and login
@app.get("/sql-connection") # Define a GET route for the /sql-connection path
async def getSQLConnection(): # Define a function to be executed when the /sql-connection path is accessed
    userInfo = findUserSQLConnectionData() # Get User's SQL Connection Data from JSON file from UniqueUserID
    # print(userInfo)
    return userInfo # Return the user's SQL Connection data


class ConnectionID(BaseModel): # Define a Pydantic model to validate the request body
    ID: str # Define an ID field of type string


@app.post("/sql-query-top") # Define a POST route for the /sql-query-top path
async def sqlQueryTop(ConnectionID: ConnectionID): # Define a function to be executed when the /sql-query-top path is accessed
    connection_info = findUserSpecificSQLConnectionData(ConnectionID.ID) # Get User's Specific SQL Connection Data from JSON file from UniqueUserID and ConnectionID
    if connection_info: # Check if the connection information is found
        required_keys = ['Driver', 'Server', 'Database', 'Table'] # Define the required keys
        filtered_connection_info = {k: v for k, v in connection_info.items() if k in required_keys} # Filter the connection information

        # Retrieve data from the database
        data,column_names = SQLConnection.getTop5Data(**filtered_connection_info) # Get the top 5 data and column names
        
        # Convert each row into a dictionary
        data_dicts = [dict(zip(column_names, row)) for row in data] # Convert each row into a dictionary

        return {"data": data_dicts} # Return the data as a list of dictionaries
    else:
        return {"error": "Connection not found"} # Return an error message if the connection is not found


class ConnectionDescription(BaseModel): # Define a Pydantic model to validate the request body
    ID: str # Define an ID field of type string
    Description: str # Define a Description field of type string

#Adding Description
@app.post("/add-description") # Define a POST route for the /add-description path
async def addTableDescription(connection: ConnectionDescription): # Define a function to be executed when the /add-description path is accessed
    try:
        addDescription(connection.ID, connection.Description) # Add/Edit Description in JSON file
        # print(connection.Description)
        return {"status": "success"} # Return a success message
    except Exception as e: 
        return {"status": "failed"} # Return a failed message
    
@app.get("/sql-refresh") # Define a GET route for the /sql-refresh path
async def sqlRefresh(): # Define a function to be executed when the /sql-refresh path is accessed
    driver, server, database = refreshSQLConnectionData() # Refresh the SQL Connection Data from JSON file from UniqueUserID
    tableNames, info = SQLConnection.getTableName(driver, server, database) # Get the table names and connection information 
    storeAllUserSQLConnectionData(tableNames, info) # Store all User's SQL Connection Data in JSON file
    SQLConnection.storeSQLInStorage(tableNames, info) # Store the SQL Connection Data in the SQLConnection folder

    sqlConnectionData = findUserSQLConnectionData() # Get User's SQL Connection Data from JSON file from UniqueUserID
    return sqlConnectionData # Return the user's SQL Connection data

#____________________AI CHATBOT____________________
class ChatbotMessage(BaseModel): # Define a Pydantic model to validate the request body
    message: str # Define a message field of type string

@app.post("/chatbot") # Define a POST route for the /chatbot path
async def messageWithAI(chatbot: ChatbotMessage): # Define a function to be executed when the /chatbot path is accessed
    response, encodedImage = AI.getUserMessage(UniqueUserID, chatbot.message) # Get User's Message with AI from JSON file from UniqueUserID
    # print("_"*100)
    # print(response)
    return response, encodedImage # Return the response message with AI

@app.get("/chatbot") # Define a GET route for the /chatbot path
async def getChatbot():  # Define a function to be executed when the /chatbot path is accessed
    history = getUserHistoryMessageWithAI() # Get User's History Message with AI from JSON file from UniqueUserID
    # print(history)
    return history # Return the history message with AI

#User can select different dataset to train the AI
#Steps:
#1. User navigate to AI Page
#2. User click on Train AI button
#3. System will retrieve all the table from the database including their name and selection status
#4. User can select the table they want to train the AI
#5. System will read user selection and update the JSON file
#6. AI will know what table to train using the selection status in the JSON file
#7. System should be starting a new AI session since the user has selected a new table

@app.get("/ai-train") # Define a GET route for the /ai-train path
async def getTrainingTableList(): # Define a function to be executed when the /ai-train path is accessed
    trainingTable = getUserTrainingTableData() # Get User's Training Table Data from JSON file from UniqueUserID
    # print("Giving:::::")
    # print(trainingTable)
    return trainingTable # Return the training table data

@app.post("/ai-train") # Define a POST route for the /ai-train path
async def trainAI(tables : List[TrainTable]): # Define a function to be executed when the /ai-train path is accessed
    AI.newChat(UniqueUserID) #Start a new AI session for the user since the system prompts will be different
    # print("Getting:::::")
    allTableName = [] # Initialize an array to store all table names
    for table in tables: # Iterate through the tables
        # print("Table", table.Table, " is set to ", table.ToTrain)
        updateTrainingTableData(table) # Update Training Table Data in JSON file 
        if table.ToTrain == "Yes": # Check if the table is set to train
            allTableName.append(table.Table) # Append the table name to the array

    driver, server, database = refreshSQLConnectionData() # Refresh the SQL Connection Data from JSON file from UniqueUserID
    tableNames, info = SQLConnection.getTableName(driver, server, database) # Get the table names and connection information

    # print("Here are all the trainable table name", allTableName)
    
    SQLConnection.storeTrainingDataset(allTableName, info) # Store the training dataset in the SQLConnection folder

    # for table in tables:
    #     if table.ToTrain == "Yes":
    #         print("Table", table.Table, " is set to ", table.ToTrain)
    #         AI.trainAI(UniqueUserID, table.Table)
    #         print("Training AI for ", table.Table)

    #Should be having a session where the new system prompt is generated

    return {"status": "Data received successfully"} if tables else {"status": "Data not received"} # Return a success message if the data is received