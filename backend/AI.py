import base64
import csv
import time
import ollama
import json
import os
import TransformingResponse as tr

#______________________________________________INTRODUCTION____________________________________________________________
#This branch and file is using Ollama API to generate the response for the user based on the history of the conversation
#The AI model used is llama3 by meta, using 8b of parameters (originally is 70b of parameters)
#llama3 will be downloaded into local and run in the local machine, hence, privacy is maintained
#However, 70b of parameters (20GB) is too large to run in the local machine, hence, 8b of parameters (5GB) is used

#______________________________________________PROCESS_________________________________________________________________
#Train the model by changing the system prompt  
#Provided the history of the conversation used as a template for the model to generate the response (FINE TUNE)
#The model will generate the response based on the history of the conversation

cwd = os.getcwd() #Store a global variable for the current working directory (To ensure workability in different machine)
relativePathForHistory = "DataStorage\\AISessionHistory" #Relative path for the history of the conversation
folderPathForHistory = os.path.join(cwd, relativePathForHistory) #Join above two path to get the full path


def get_csv_column_names(file_path): #Function to get the column names of the csv file
    with open(file_path, 'r', newline='') as file: #Open the file
        reader = csv.reader(file) #Read the file
        column_names = next(reader) #Read the first row to get the column names
    return column_names

def getSystemPrompt(): #Function to get the system prompt
    relativePath = "TrainingTable" #This is the folder where the training-required csv files are stored
    folderPath = os.path.join(cwd, relativePath) #Join the current working directory with the relative path to get the full path
    files = os.listdir(folderPath) #Get the list of files in the folder
    fileNames = [file for file in files if os.path.isfile(os.path.join(folderPath, file))] #Get the list of files that are files only

    arr = [] #Create an empty array to store the column names of the csv files
    for file in fileNames: #Loop through the list of files
        folderssPath = f"{folderPath}\\{file}" #Get the full path of the file
        columns = get_csv_column_names(folderssPath) #Get the column names of the file
        columns_str = ', '.join(columns) #Join the column names with a comma
        value = file + " have " + columns_str #Get the file name and the column names
        arr.append(value) #Append the value to the array

    systemContext = f"""
    1. You are a data visualization expertise which done perfect code for visualization in python. You are now providing only code for a client who may ask question based on the data that you are train on. You should only provides code. Start the code by importing the necessary library. Then, read the csv file into pandas DataFrame. Group the data based on the requirement, save the visualization as image with a name of chart.png and show the image.
    2. Your system has {len(files)} files. 
    3. The files are {fileNames}. 
    4. Each files have different columns. Here are the columns in each file. {arr} 
    5. Based on that, whenever you are reading the csv file, you should use the existing column from the csv you read. You are not allowed to create a column of a specific table to make your code works. All the visualization must come from related table and existing column of the table. Refer {arr} for the columns in each file.
    6. You should only provide python code which is use to show the visualization.Ensure the code is working perfectly without any error. Visualization should have title, label, x and y axis. 
    7. The visualization should be able to save as image. The image must be saved as a name of \"chart.png\". 
    8. When reading the csv into pandas DataFrame, add {folderPath} as the path and followed by whatever csv file to let the user to be able to run the code. The path should be like {folderPath}\\\"the csv file suits with requirement\".
    9. You should not provide any explanation or context of your code, only code is provided. You should not provide any code that is not related to the visualization. You should not provide any code that is not working. You should not provide any code that is not in python. You should not provide any code that is not related to the data that you are train on. You should not provide any code that is not related to the data visualization.
    """ #The system prompt that will be used to train the model

    return systemContext 

#Function that modify the system context

def newChat(UUID): #Function to start a new chat
    toWriteJson = { #Create a dictionary to store the data
        "id": UUID, #Store the UUID
        "history": [], #Store the history of the conversation
        "context": [], #Store the context of the conversation
    }
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as jsonFile: #Open the json file
        json.dump(toWriteJson, jsonFile, indent=4) #Dump the data into the json file

def getUserMessage(UUID, message): #Function to get the user message and chat with the AI
    toStoreJson = { #Create a dictionary to store the user message in history
        "role": "user",
        "content": message,
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file: #Open the json file
        data = json.load(file) #Load the data
        data["history"].append(toStoreJson) #Append the user message to the history
        
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file: #Open the json file
        json.dump(data, file, indent=4) #Dump the data into the json file

    response, encodedImage = chatWithLlama3(UUID, message) #Chat with the AI
  
    return response, encodedImage
    
def chatWithLlama3(UUID, message): #Function to chat with the AI
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file: #Open the json file
        data = json.load(file) #Load the data
        context = data["context"] #Get the context of the conversation

    #This is the history of conversation to be used in ollama.chat function
    # msgs=[
    #     {"role": "system", "content": getSystemPrompt()},
    #     {"role": "user", "content": "draw me a bar chart of total orders based on customer id"},
    #     {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norders_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\Orders.csv\")\ntotal_orders = orders_df.groupby('CustomerID')['OrderID'].count().reset_index(name='Total Orders')\n\nplt.bar(total_orders['CustomerID'], total_orders['Total Orders'])\nplt.xlabel('Customer ID')\nplt.ylabel('Total Orders')\nplt.title('Total Orders by Customer ID')\nplt.savefig('chart.png')\n```"},
    #     {"role": "user", "content": "draw me a bar chart of total orders based on different product"},
    #     {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norder_details_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\OrderDetails.csv\")\n\n# Calculate total sales per product\norder_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']\nproduct_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()\n\n# Plot the total sales\nplt.figure(figsize=(10, 6))\nplt.bar(product_sales['ProductID'].astype(str), product_sales['TotalSales'], color='skyblue')\nplt.xlabel('Product ID')\nplt.ylabel('Total Sales')\nplt.title('Total Sales by Product')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.savefig('chart.png')\n```"},
    #     {"role": "user", "content": message},
    # ]

    #Previous system prompt 
    # output = ollama.chat(
    #     model='llama3',
    #     messages = msgs,
    #     stream=True,
    # )

    #This is the history of conversation to be used in ollama.generate function
    #This will form a better response from the AI
    msgsInGenerateContent=[ 
        # {"role": "system", "content": getSystemPrompt()},
        "input: draw me a bar chart of total orders based on customer id",
        "output: ```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norders_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\Orders.csv\")\ntotal_orders = orders_df.groupby('CustomerID')['OrderID'].count().reset_index(name='Total Orders')\n\nplt.bar(total_orders['CustomerID'], total_orders['Total Orders'])\nplt.xlabel('Customer ID')\nplt.ylabel('Total Orders')\nplt.title('Total Orders by Customer ID')\nplt.savefig('chart.png')\n```",
        "input: draw me a bar chart of total orders based on different product",
        "output: ```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norder_details_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\OrderDetails.csv\")\n\n# Calculate total sales per product\norder_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']\nproduct_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()\n\n# Plot the total sales\nplt.figure(figsize=(10, 6))\nplt.bar(product_sales['ProductID'].astype(str), product_sales['TotalSales'], color='skyblue')\nplt.xlabel('Product ID')\nplt.ylabel('Total Sales')\nplt.title('Total Sales by Product')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.savefig('chart.png')\n```",
    ]

    #This is the prompt for the AI to generate the response
    prompt = f"""Here is the history of the correct version of code that you should provide: {msgsInGenerateContent}.
    This is the system instruction you should follow: {getSystemPrompt()}.
    Here is the question that you should provide the code: {message}
    """

    output = ollama.generate( #Generate the response from the AI
        model='llama3', #Use the llama3 model
        prompt = prompt, #Use the prompt to generate the response
        # system= getSystemPrompt(),
        stream=True, #Stream the response
    )

    response = "" #Initialize the response

    for chunk in output:
        print(chunk['response'], end='', flush=True) #Print the output in chunks
        response += chunk['response'] #Get the response
        if(chunk['done'] ==True):
            toWriteContext = context + chunk['context'] #Get the context of the conversation

    syntaxErrorCheckingResult, nothingError, nothingFatal, runtimeError = tr.transformResponse(response) #Transform the response

    while(nothingError == "Error found" or nothingFatal == "Fatal found" or runtimeError != "No runtime errors"): # If error exists, passed the error to the AI to reprompt
        print("There is an error in the code") # Print the error message
        print("Here is the error code: ", response) # Print the error code
        syntaxError = "" # Initialize the syntax error
        syntaxFatal = "" # Initialize the syntax fatal
        runtimeErrorText = "" # Initialize the runtime error text
        if(syntaxErrorCheckingResult['Error'] != []): # Check if there are any errors
            for error in syntaxErrorCheckingResult['Error']: # Loop through the errors in syntax error checking result
                syntaxError += error # Append the error to the syntax error
        else:
            syntaxError = None # Set the syntax error to None
        
        if(syntaxErrorCheckingResult['Fatal'] != []): # Check if there are any fatal
            for fatal in syntaxErrorCheckingResult['Fatal']: # Loop through the fatals in syntax error checking result
                syntaxFatal += fatal # Append the fatal to the syntax fatal
        else: 
            syntaxFatal = None # Set the syntax fatal to None

        if(runtimeError != "No runtime errors"): # Check if there are any runtime errors
            runtimeErrorText = runtimeError # Set the runtime error text to the runtime error
        else: # If there are no runtime errors
            runtimeErrorText = None # Set the runtime error text to None

        print("Syntax Error: ", syntaxError, '\n') # Print the syntax error
        print("Syntax Fatal: ", syntaxFatal, '\n') # Print the syntax fatal
        print("Runtime Error: ", runtimeErrorText, '\n') # Print the runtime error

        prompt = f""" 
        The code that you provided is having error. Here are the errors: 
        Syntax Error: {syntaxError}
        Syntax Fatal: {syntaxFatal}
        Runtime Error: {runtimeErrorText}
        Here are the history of the correct version of code that you should provide: {msgsInGenerateContent}
        Here is the question that you should provide the code: {message}
        Please provide the correct code based on the system instruction.
        """ # Change the prompt to reprompt request

        output = ollama.generate( #Generate the response from the AI
            model='llama3', #Use the llama3 model
            prompt = prompt, #Use the prompt to generate the response
            # system= getSystemPrompt(),
            stream=True, #Stream the response
        )

        response = "" #Initialize the response

        for chunk in output:
            print(chunk['response'], end='', flush=True) #Print the output in chunks
            response += chunk['response'] #Get the response
            if(chunk['done'] ==True):
                toWriteContext = context + chunk['context'] #Get the context of the conversation

        syntaxErrorCheckingResult, nothingError, nothingFatal, runtimeError = tr.transformResponse(response) #Transform the response

    time.sleep(5)# wait for the image to be generated and saved in our local machine

    image_file = open("chart.png", "rb") #Open the image file

    encodedImage = base64.b64encode(image_file.read()).decode('utf-8') #Encode the image file to base64 format

    toStoreJson = { #Create a dictionary to store the data, this will be used as a history of the conversation
        "role": "AI",
        "content": encodedImage,
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file: #Open the json file
        data = json.load(file)  #Load the data  
        data["history"].append(toStoreJson) #Append the AI response to the history
        data["context"] = toWriteContext #Store the context of the conversation

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file: #Open the json file
        json.dump(data, file, indent=4) #Dump the data into the json file
    return response, encodedImage


#______________________________________________FUTURE ENHANCEMENT_________________________________________________________________
#Keep the response as a python seperate file since the response will be a python runnale code
#All the code generated by the AI should be store in a seperate folder, where the folder name should be the UniqueID from user
#Each user folder should be stored in a master folder to keep neat and tidy

#Process will be like:
#1. User send a message to the AI
#2. AI will generate a response
#3. System will store the response in a python file
#4. To use the python file to show the visualization, user should provide a name to label the python file, which is the visualization

#Therefore, there should be having a user json file to store each python file name and their title
#Sturcture of the json file:
#{ "UniqueID": "123ABC","Visualization": [{"Visualization": "Title1", FileName:"oaijewf.py"}, {"Visualization": "Title2", FileName:"iuhgieaf.py"}]}
