import ollama
import pandas as pd
import random
import string
import json
import os

#Train the model by changing the system prompt (NOT FINE TUNE)
cwd = os.getcwd()

relativePath = "TableStorage"

folderPath = os.path.join(cwd, relativePath)
files = os.listdir(folderPath)
fileNames = [file for file in files if os.path.isfile(os.path.join(folderPath, file))]
dataFrame = [pd.read_csv(f"{folderPath}\\{fileName}") for fileName in fileNames]
dataTypeOfColumnInDataFrame = [df.dtypes for df in dataFrame]

relativePathForHistory = "DataStorage\\AISessionHistory"
folderPathForHistory = os.path.join(cwd, relativePathForHistory)

systemContext = f"Your system has {len(files)} files. The files are {fileNames}. The data type of the columns in the files are {dataTypeOfColumnInDataFrame}. You are a data visualization expertise which done perfect code in python. You are now providing only code for a client who may ask question based on the data that you are train on. You should only provide python code which is use to show the visualization. Ensure the code is working perfectly without any error. Visualization should have title, label, x and y axis. The visualization should be able to save as image. You should not provide any explanation or context of your code, only code is provided. You should not provide any code that is not related to the visualization. You should not provide any code that is not working. You should not provide any code that is not in python. You should not provide any code that is not related to the data that you are train on. You should not provide any code that is not related to the data visualization."

def newChat(UUID):
    toWriteJson = {
        "id": UUID,
        "history": [],
        "context": [],
    }
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as jsonFile:
        json.dump(toWriteJson, jsonFile, indent=4)
    # Rest of your code

def getUserMessage(UUID, message):
    toStoreJson = {
        "role": "user",
        "content": message,
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file:
        data = json.load(file) 
        data["history"].append(toStoreJson)
        
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file:
        json.dump(data, file, indent=4)

    response = chatWithLlama3(UUID, message)

    return response
    
def chatWithLlama3(UUID, message):
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file:
        data = json.load(file) 
        context = data["context"]
    
    output = ollama.generate(
        model='llama3',
        prompt = message,
        system= systemContext,
        stream=True,      
        context= context,  
    )

    response = ""

    for chunk in output:
        print(chunk['response'], end='', flush=True)
        response += chunk['response']
        if chunk['done'] == True:
            toWriteContext = context + chunk['context']
        
    toStoreJson = {
        "role": "AI",
        "content": response,
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file:
        data = json.load(file) 
        data["history"].append(toStoreJson)
        data["context"] = toWriteContext

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file:
        json.dump(data, file, indent=4)

    return response

