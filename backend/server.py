from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import SQLConnection
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import random
import AI
import glob
import pandas as pd

app = FastAPI() #Create a FastAPI instance

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


@app.get("/") #Root API
def read_root(): #Function to read the root API
    return {"Welcome to": "Ollama version"} #Return the welcome message

global UniqueUserID #Globalized UniqueUserID to be used in the whole application
UniqueUserID = "" #Initialized UniqueUserID to empty string

#____________________LOGIN____________________
class UserCredentials(BaseModel): #Model for User Credentials
    username: str
    password: str

@app.post("/login") #Login API
async def login(user: UserCredentials): #Function to login
    login = False #Initialized login to False (Future Use)
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\UserCredential" #Set the relative path to the UserCredential folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UserName"] == user.username and userInfo["Password"] == user.password: #Check if the username and password is correct
                    global UniqueUserID #Globalized UniqueUserID to be used in the whole application
                    UniqueUserID = userInfo["UniqueUserID"] #Set the UniqueUserID to the user's UniqueUserID
                    # print("UniqueUserID: " + UniqueUserID)   
                    login = True #Set login to True (Future Use)
                    return {"status": "success", "UniqueUserID": userInfo["UniqueUserID"]} #Return success message and the UniqueUserID to frontend
                
    #If user not found, should:
    #1. Return a message to the user that the username or password is incorrect and require admin to register
    #2. Lead to register page

    return {"status": "failed"} #Return failed message if the username or password is incorrect

#____________________DATA RETRIEVAL____________________
#Get User's SQL Connection Data from JSON file from UniqueUserID
def findUserSQLConnectionData(): #Function to find the user's SQL Connection Data
    # print("UniqueUserID: " + UniqueUserID)
    #Temporary local storage of JSON file 
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UniqueUserID"] == UniqueUserID: #Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    # print(userInfo)
                    return userInfo #Return the user's SQL Conncetion Data
    return None #Return None if the user's SQL Connection Data is not found

def findUserSpecificSQLConnectionData(id: str): #Function to find the user's specific SQL Connection Data
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UniqueUserID"] == UniqueUserID: #Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    driver = str(userInfo["Driver"]) #Get the driver from the JSON file
                    server = str(userInfo["Server"]) #Get the server from the JSON file
                    database = str(userInfo["Database"]) #Get the database from the JSON file
                    for connection in userInfo["Connection"]: #Loop through the connection (Which stores all the table info in the database) in the JSON file
                        if connection["ConnectionID"] == id: #Check if the ConnectionID in the JSON file is the same as the user's ConnectionID
                            # Convert non-string values to strings
                            connection_info = { #Store the connection info in a dictionary
                                "ConnectionID": str(connection["ConnectionID"]), #Get the ConnectionID from the JSON file
                                "Driver": driver, #Get the driver from the JSON file
                                "Server": server, #Get the server from the JSON file
                                "Database": database, #Get the database from the JSON file
                                "Table": str(connection["Table"]), #Get the table from the JSON file
                                "ConnectionStatus": str(connection["ConnectionStatus"]), #Get the connection status from the JSON file
                                "Description": str(connection["Description"]) #Get the description from the JSON file
                            }
                            return connection_info #Return the connection info
    return None #Return None if the user's specific SQL Connection Data is not found

def getUserTrainingTableData(): #Function to get the user's training table data
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UniqueUserID"] == UniqueUserID: #Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    toTrainTableArray = [] #Initialize the toTrainTableArray
                    for connection in userInfo["Connection"]: #Loop through the connection (Which stores all the table info in the database) in the JSON file
                        toTrainTable = { #Store the toTrainTable in a dictionary
                            "Table": connection["Table"], #Get the table from the JSON file
                            "ToTrain" : connection["ToTrain"] #Get the toTrain status from the JSON file
                        }
                        toTrainTableArray.append(toTrainTable) #Append the toTrainTable to the toTrainTableArray
                    return toTrainTableArray #Return the toTrainTableArray
    return None #Return None if the user's training table data is not found

def getUserHistoryMessageWithAI(): #Function to get the user's history message with Ai
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\AISessionHistory" #Get the relative path to the AISessionHistory folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["id"] == UniqueUserID: #Check if the id in the JSON file is the same as the user's UniqueUserID
                    # print(userInfo["history"])
                    return userInfo["history"] #Return the history from the JSON file
    return None #Return None if the user's history message with AI is not found

def refreshSQLConnectionData(): #Function to refresh the SQL Connection Data
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode 
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UniqueUserID"] == UniqueUserID: #Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    driver = str(userInfo["Driver"]) #Get the driver from the JSON file
                    server = str(userInfo["Server"]) #Get the server from the JSON file
                    database = str(userInfo["Database"]) #Get the database from the JSON file
                    return driver, server, database #Return the driver, server and database
    return None #Return None if the SQL Connection Data is not found

#____________________DATA STORAGE____________________ #Connection bridge to JSON file (Future in data storage)
class ConnectionInfo(BaseModel): #Model for Connection Info
    Driver: str 
    Server: str
    Database: str

#Generate random ID for SQL Connection
def randomID(): #Function to generate random ID
    randomAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" #Set the randomAlpha to all the alphabets
    randomNum = "0123456789" #Set the randomNum to all the numbers
    randomID = "" #Initialize the randomID to empty string 
    for i in range(0, 3): #Loop through the range of 3
        randomID += randomAlpha[random.randint(0, 51)] #Add the random alphabet to the randomID
    for i in range(0, 3): #Loop through the range of 3
        randomID += randomNum[random.randint(0, 9)] #Add the random number to the randomID
    return randomID #Return the randomID

def storeAllUserSQLConnectionData(allTableNames, info): #Function to store all the user's SQL Connection Data
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file

                toStoreJson ={ #Store the JSON data in a dictionary
                    "UniqueUserID": UniqueUserID, #Initialize the UniqueUserID to the user's UniqueUserID
                    "Driver": None, #Initialize the Driver to None
                    "Server": None, #Initialize the Server to None
                    "Database": None, #Initialize the Database to None
                    "Connection": [] #Initialize the Connection to an empty array
                }         
                if userInfo["UniqueUserID"] == UniqueUserID: #Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    toStoreJson["Driver"] = info[0] #Set the Driver to the driver from the info
                    toStoreJson["Server"] = info[1] #Set the Server to the server from the info
                    toStoreJson["Database"] = info[2] #Set the Database to the database from the info
                    for name in allTableNames: #Loop through all the table names
                        toStoreConnection = { #Store the Connection in a dictionary
                            "ConnectionID": randomID(), #Set the ConnectionID to the randomID
                            "Table": name, #Set the Table to the name which is the tableName
                            "ConnectionStatus": "Test", #Set the ConnectionStatus to Test
                            "Description": "", #Set the Description to empty string
                            "ToTrain": "Yes" #Set the ToTrain to Yes
                        } 
                        toStoreJson["Connection"].append(toStoreConnection) #Append the toStoreConnection to the Connection
                        # print(toStoreConnection)
                        # print('\n\n\n final json :')
                        # print(toStoreJson)
                    with open(os.path.join(folderPath, filename), "w") as file: #Open the file in write mode
                        json.dump(toStoreJson, file, indent=4) #Dump the toStoreJson to the file
                    break

#Add/Edit Description
def addDescription(id: str, description: str): #Function to add description
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UniqueUserID"] == UniqueUserID: # Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    for i in range(0, len(userInfo["Connection"])): #Loop through the range of the Connection
                        if userInfo["Connection"][i]["ConnectionID"] == id: #Check if the ConnectionID in the JSON file is the same as the user's ConnectionID
                            userInfo["Connection"][i]["Description"] = description #Set the Description to the description
                            with open(os.path.join(folderPath, filename), "w") as file: #Open the file in write mode
                                json.dump(userInfo, file, indent=4) #Dump the userInfo to the file
                            break

class TrainTable(BaseModel): #Model for Train Table
    Table: str
    ToTrain: str

def updateTrainingTableData(table: TrainTable): #Function to update the training table data
    cwd = os.getcwd() #Get the current working directory
    relativePath = "DataStorage\\SQLConnection_New" #Get the relative path to the SQLConnection_New folder
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    for filename in os.listdir(folderPath): #Loop through the folder to get all the files in the folder
        if filename.endswith(".json"): #Check if the file is a JSON file
            with open(os.path.join(folderPath, filename), "r") as file: #Open the file in read mode
                userInfo = json.load(file) #Load the JSON file
                if userInfo["UniqueUserID"] == UniqueUserID: #Check if the UniqueUserID in the JSON file is the same as the user's UniqueUserID
                    for i in range(0, len(userInfo["Connection"])): #Loop through the range of the Connection
                        if userInfo["Connection"][i]["Table"] == table.Table: #Check if the Table in the JSON file is the same as the user's Table
                            userInfo["Connection"][i]["ToTrain"] = table.ToTrain #Set the ToTrain to the table.ToTrain
                            with open(os.path.join(folderPath, filename), "w") as file: #Open the file in write mode
                                json.dump(userInfo, file, indent=4) #Dump the userInfo to the file
                            break

#____________________SQL CONNECTION____________________
@app.post("/sql-connection") #SQL Connection API
async def sqlConnection(connection_info: ConnectionInfo): #Function to get message to know if user successfully connect to database
    # tableNames = SQLConnection.getTableName(connection_info.driver, connection_info.server, connection_info.database)
    connectionInfo = {k: v for k,v in connection_info} #Get the connection info
    # print(connectionInfo)
    tableNames, info = SQLConnection.getTableName(**connectionInfo) #Get the table names and info from the SQL Connection
    storeAllUserSQLConnectionData(tableNames, info) #Store all the user's SQL Connection Data
    SQLConnection.storeSQLInStorage(tableNames, info) #Store the SQL Data in the storage
    return {"status": "success"} #Return success message

@app.get("/sql-connection") #SQL Connection API
async def getSQLConnection(): #Function to get User's SQL Connection Data when user refresh the page and login
    userInfo = findUserSQLConnectionData() #Find the user's SQL Connection Data
    # print(userInfo)
    return userInfo #Return the user's SQL Connection Data

class ConnectionID(BaseModel):
    ID: str

@app.post("/sql-query-top") #SQL Query Top API
async def sqlQueryTop(ConnectionID: ConnectionID): #Function to get the top 5 data from the table
    connection_info = findUserSpecificSQLConnectionData(ConnectionID.ID) #Find the user's specific SQL Connection Data
    if connection_info: #Check if the connection info is found
        required_keys = ['Driver', 'Server', 'Database', 'Table'] #Set the required keys
        filtered_connection_info = {k: v for k, v in connection_info.items() if k in required_keys} #Filter the connection info

        # Retrieve data from the database
        data,column_names = SQLConnection.getTop5Data(**filtered_connection_info) #Get the top 5 data and column names from the SQL Connection
        
        # Convert each row into a dictionary
        data_dicts = [dict(zip(column_names, row)) for row in data] #Convert each row into a dictionary

        return {"data": data_dicts} #Return the data dictionary
    else:
        return {"error": "Connection not found"} #Return error message if the connection is not found


class ConnectionDescription(BaseModel): #Model for Connection Description
    ID: str
    Description: str

#Adding Description
@app.post("/add-description") #Add Description API
async def addTableDescription(connection: ConnectionDescription): #Function to add table description
    try:
        addDescription(connection.ID, connection.Description) #Call the addDescription function
        # print(connection.Description) 
        return {"status": "success"} #Return success message
    except Exception as e: #If there is an error occur, print out the error
        return {"status": "failed"}
    
@app.get("/sql-refresh") #SQL Refresh API
async def sqlRefresh(): #Function to refresh the SQL Connection Data
    driver, server, database = refreshSQLConnectionData() #Refresh the SQL Connection Data
    tableNames, info = SQLConnection.getTableName(driver, server, database) #Get the table names and info from the SQL Connection
    storeAllUserSQLConnectionData(tableNames, info) #Store all the user's SQL Connection Data
    SQLConnection.storeSQLInStorage(tableNames, info) #Store the SQL Data in the storage

    sqlConnectionData = findUserSQLConnectionData() #Find the user's SQL Connection Data
    return sqlConnectionData

#____________________AI CHATBOT____________________
class ChatbotMessage(BaseModel): #Model for Chatbot Message
    message: str

@app.post("/chatbot") #Chatbot API
async def messageWithAI(chatbot: ChatbotMessage): #Function to get message from user and response from AI
    response, encodedImage = AI.getUserMessage(UniqueUserID, chatbot.message) #Get the response and encoded image from AI
    # print("_"*100)
    # print(response)
    return response, encodedImage #Return the response and encoded image

@app.get("/chatbot") #Chatbot API
async def getChatbot(): #Function to get the chatbot message
    history = getUserHistoryMessageWithAI() #Get the user's history message with AI 
    # print(history)
    return history #Return the history

#User can select different dataset to train the AI
#Steps:
#1. User navigate to AI Page
#2. User click on Train AI button
#3. System will retrieve all the table from the database including their name and selection status
#4. User can select the table they want to train the AI
#5. System will read user selection and update the JSON file
#6. AI will know what table to train using the selection status in the JSON file
#7. System should be starting a new AI session since the user has selected a new table

@app.get("/ai-train") #AI Train API
async def getTrainingTableList(): #Function to get the training table list
    trainingTable = getUserTrainingTableData() #Get the user's training table data
    # print("Giving:::::")
    # print(trainingTable)
    return trainingTable #Return the training table

@app.post("/ai-train") #AI Train API
async def trainAI(tables : List[TrainTable]): #Function to train AI
    AI.newChat(UniqueUserID) #Start a new AI session for the user since the system prompts will be different
    # print("Getting:::::")
    allTableName = [] #Initialize the allTableName to an empty array
    for table in tables: #Loop through the tables
        # print("Table", table.Table, " is set to ", table.ToTrain)
        updateTrainingTableData(table) #Update the training table data
        if table.ToTrain == "Yes": #Check if the table is set to Yes
            allTableName.append(table.Table) #Append the table name to the allTableName

    driver, server, database = refreshSQLConnectionData() #Refresh the SQL Connection Data
    tableNames, info = SQLConnection.getTableName(driver, server, database) #Get the table names and info from the SQL Connection

    # print("Here are all the trainable table name", allTableName)
    
    SQLConnection.storeTrainingDataset(allTableName, info) #Store the training dataset

    # for table in tables:
    #     if table.ToTrain == "Yes":
    #         print("Table", table.Table, " is set to ", table.ToTrain)
    #         AI.trainAI(UniqueUserID, table.Table)
    #         print("Training AI for ", table.Table)

    #Should be having a session where the new system prompt is generated

    return {"status": "Data received successfully"} if tables else {"status": "Data not received"} #Return success message if the data is received successfully 