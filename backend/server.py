from fastapi import FastAPI
from pydantic import BaseModel
import SQLConnection
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import random
import AI
import glob

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"Hello": "World"}

global UniqueUserID
UniqueUserID = ""

#____________________LOGIN____________________
class UserCredentials(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(user: UserCredentials):
    login = False
    cwd = os.getcwd()
    relativePath = "DataStorage\\UserCredential"
    folderPath = os.path.join(cwd, relativePath)
    for filename in os.listdir(folderPath):
        if filename.endswith(".json"):
            with open(os.path.join(folderPath, filename), "r") as file:
                userInfo = json.load(file)                
                if userInfo["UserName"] == user.username and userInfo["Password"] == user.password:
                    global UniqueUserID
                    UniqueUserID = userInfo["UniqueUserID"]        
                    print("UniqueUserID: " + UniqueUserID)   
                    login = True         
                    return {"status": "success", "UniqueUserID": userInfo["UniqueUserID"]}
                
    #If user not found, should:
    #1. Return a message to the user that the username or password is incorrect and require admin to register
    #2. Lead to register page
    return {"status": "failed"}

#____________________DATA RETRIEVAL____________________
#Get User's SQL Connection Data from JSON file from UniqueUserID
def findUserSQLConnectionData():
    print("UniqueUserID: " + UniqueUserID)
    #Temporary local storage of JSON file 
    cwd = os.getcwd()
    relativePath = "DataStorage\\SQLConnection_New"
    folderPath = os.path.join(cwd, relativePath)
    for filename in os.listdir(folderPath):
        if filename.endswith(".json"):
            with open(os.path.join(folderPath, filename), "r") as file:
                userInfo = json.load(file)                
                if userInfo["UniqueUserID"] == UniqueUserID:
                    print(userInfo)
                    return userInfo
    return None

def findUserSpecificSQLConnectionData(id: str):
    cwd = os.getcwd()
    relativePath = "DataStorage\\SQLConnection_New"
    folderPath = os.path.join(cwd, relativePath)
    for filename in os.listdir(folderPath):
        if filename.endswith(".json"):
            with open(os.path.join(folderPath, filename), "r") as file:
                userInfo = json.load(file)
                if userInfo["UniqueUserID"] == UniqueUserID:
                    driver = str(userInfo["Driver"])
                    server = str(userInfo["Server"])
                    database = str(userInfo["Database"])
                    for connection in userInfo["Connection"]:                    
                        if connection["ConnectionID"] == id:
                            # Convert non-string values to strings
                            connection_info = {
                                "ConnectionID": str(connection["ConnectionID"]),
                                "Driver": driver,
                                "Server": server,
                                "Database": database,
                                "Table": str(connection["Table"]),
                                "ConnectionStatus": str(connection["ConnectionStatus"]),
                                "Description": str(connection["Description"])
                            }
                            return connection_info
    return None


def getUserHistoryMessageWithAI():
    cwd = os.getcwd()
    relativePath = "DataStorage\\AISessionHistory"
    folderPath = os.path.join(cwd, relativePath)
    for filename in os.listdir(folderPath):
        if filename.endswith(".json"):
            with open(os.path.join(folderPath, filename), "r") as file:
                userInfo = json.load(file)                
                if userInfo["id"] == UniqueUserID:
                    print(userInfo["history"])
                    return userInfo["history"]
    return None
#____________________DATA STORAGE____________________ #Connection bridge to JSON file (Future in data storage)
class ConnectionInfo(BaseModel):
    Driver: str
    Server: str
    Database: str

#Generate random ID for SQL Connection
def randomID():
    randomAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    randomNum = "0123456789"
    randomID = ""
    for i in range(0, 3):
        randomID += randomAlpha[random.randint(0, 51)]
    for i in range(0, 3):
        randomID += randomNum[random.randint(0, 9)]
    return randomID

def storeAllUserSQLConnectionData(allTableNames, info):
    cwd = os.getcwd()
    relativePath = "DataStorage\\SQLConnection_New"
    folderPath = os.path.join(cwd, relativePath)
    for filename in os.listdir(folderPath):
        if filename.endswith(".json"):
            with open(os.path.join(folderPath, filename), "r") as file:
                userInfo = json.load(file)                
                if userInfo["UniqueUserID"] == UniqueUserID:
                    userInfo["Driver"] = info[0]
                    userInfo["Server"] = info[1]
                    userInfo["Database"] = info[2]
                    tableNameInFile = [connection["Table"] for connection in userInfo["Connection"]]
                    for name in allTableNames:
                        if name in tableNameInFile:
                            continue
                        else:
                            connection = {
                                "ConnectionID": randomID(),
                                "Table": name,
                                "ConnectionStatus": "Test",
                                "Description": ""
                            }
                            userInfo["Connection"].append(connection)
                            print(connection)
                        print(userInfo)
                    with open(os.path.join(folderPath, filename), "w") as file:
                        json.dump(userInfo, file, indent=4)
                    break

#Add/Edit Description
def addDescription(id: str, description: str):
    cwd = os.getcwd()
    relativePath = "DataStorage\\SQLConnection_New"
    folderPath = os.path.join(cwd, relativePath)
    for filename in os.listdir(folderPath):
        if filename.endswith(".json"):
            with open(os.path.join(folderPath, filename), "r") as file:
                userInfo = json.load(file)                
                if userInfo["UniqueUserID"] == UniqueUserID:
                    for i in range(0, len(userInfo["Connection"])):
                        if userInfo["Connection"][i]["ConnectionID"] == id:
                            userInfo["Connection"][i]["Description"] = description
                            with open(os.path.join(folderPath, filename), "w") as file:
                                json.dump(userInfo, file, indent=4)
                            break


#____________________SQL CONNECTION____________________

#Get message to know if user successfully connect to database
@app.post("/sql-connection")
async def sqlConnection(connection_info: ConnectionInfo):
    # tableNames = SQLConnection.getTableName(connection_info.driver, connection_info.server, connection_info.database)
    connectionInfo = {k: v for k,v in connection_info}
    print(connectionInfo)
    tableNames, info = SQLConnection.getTableName(**connectionInfo)
    storeAllUserSQLConnectionData(tableNames, info) 
    SQLConnection.storeSQLInStorage(tableNames, info)

    return {"status": "success"}

#Get User's SQL Connection Data when user refresh the page and login
@app.get("/sql-connection")
async def getSQLConnection():
    userInfo = findUserSQLConnectionData()
    print(userInfo)
    return userInfo


class ConnectionID(BaseModel):
    ID: str


@app.post("/sql-query-top")
async def sqlQueryTop(ConnectionID: ConnectionID):
    connection_info = findUserSpecificSQLConnectionData(ConnectionID.ID)
    if connection_info:
        required_keys = ['Driver', 'Server', 'Database', 'Table']
        filtered_connection_info = {k: v for k, v in connection_info.items() if k in required_keys}

        # Retrieve data from the database
        data,column_names = SQLConnection.getTop5Data(**filtered_connection_info)
        
        # Convert each row into a dictionary
        data_dicts = [dict(zip(column_names, row)) for row in data]

        return {"data": data_dicts}
    else:
        return {"error": "Connection not found"}


class ConnectionDescription(BaseModel):
    ID: str
    Description: str

#Adding Description
@app.post("/add-description")
async def addTableDescription(connection: ConnectionDescription):
    try:
        addDescription(connection.ID, connection.Description)
        print(connection.Description)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed"}
    

#____________________AI CHATBOT____________________
class ChatbotMessage(BaseModel):
    message: str

@app.post("/chatbot")
async def messageWithAI(chatbot: ChatbotMessage):
    response = AI.getUserMessage(UniqueUserID, chatbot.message)
    print("_"*100)
    print(response)
    return response

@app.get("/chatbot")
async def getChatbot():
    history = getUserHistoryMessageWithAI()
    print(history)
    return history

