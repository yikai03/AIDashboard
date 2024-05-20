import ollama
import pandas as pd
import random
import string
import json

def generate_random_id(length):
    characters = string.ascii_letters + string.digits
    randomId = ''.join(random.choice(characters) for _ in range(length))
    return randomId

def newChat():
    randomId = generate_random_id(10)

    toWriteJson = {
        "id": randomId,
        "history": [],
        "context": [],
    }
    with open(f"backend/DataStorage/AISessionHistory/{randomId}.json", "w") as jsonFile:
        json.dump(toWriteJson, jsonFile, indent=4)
    # Rest of your code

def getUserMessage(id, message):
    toStoreJson = {
        "role": "user",
        "content": message,
    }

    with open(f"backend/DataStorage/AISessionHistory/{id}.json", "r") as file:
        data = json.load(file) 
        data["history"].append(toStoreJson)
        
    with open(f"backend/DataStorage/AISessionHistory/{id}.json", "w") as file:
        json.dump(data, file, indent=4)

    chatWithLlama3(id, message)


    
def chatWithLlama3(id, message):
    with open(f"backend/DataStorage/AISessionHistory/{id}.json", "r") as file:
        data = json.load(file) 
        context = data["context"]
    
    output = ollama.generate(
        model='llama3',
        prompt = message,
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

    with open(f"backend/DataStorage/AISessionHistory/{id}.json", "r") as file:
        data = json.load(file) 
        data["history"].append(toStoreJson)
        data["context"] = toWriteContext
        
    with open(f"backend/DataStorage/AISessionHistory/{id}.json", "w") as file:
        json.dump(data, file, indent=4)

    return response

