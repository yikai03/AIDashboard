import base64
import csv
import time
import ollama
import pandas as pd
import random
import string
import json
import os
import TransformingResponse as tr

#Train the model by changing the system prompt (NOT FINE TUNE)
cwd = os.getcwd()
relativePathForHistory = "DataStorage\\AISessionHistory"
folderPathForHistory = os.path.join(cwd, relativePathForHistory)


def get_csv_column_names(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        # Read the first row
        column_names = next(reader)
    return column_names

def getSystemPrompt():
    relativePath = "TrainingTable"
    folderPath = os.path.join(cwd, relativePath)
    files = os.listdir(folderPath)
    fileNames = [file for file in files if os.path.isfile(os.path.join(folderPath, file))]
    dataFrame = [pd.read_csv(f"{folderPath}\\{fileName}") for fileName in fileNames]
    columnNameOfDataFrame = [df.columns for df in dataFrame]
    dataTypeOfColumnInDataFrame = [df.dtypes for df in dataFrame]
    # print(fileNames)
    # print(dataFrame)
    # print(columnNameOfDataFrame)
    # print(dataTypeOfColumnInDataFrame)

    arr = []
    for file in fileNames:
        folderssPath = f"{folderPath}\\{file}"
        columns = get_csv_column_names(folderssPath)
        columns_str = ', '.join(columns)
        value = file + " have " + columns_str
        arr.append(value)

    # print(arr)

    systemContext = f"""
    1. You are a data visualization expertise which done perfect code for visualization in python. You are now providing only code for a client who may ask question based on the data that you are train on. You should only provides code. Start the code by importing the necessary library. Then, read the csv file into pandas DataFrame. Group the data based on the requirement, show the visualization, save the visualization as image with a name of chart.png and show the image.
    2. Your system has {len(files)} files. 
    3. The files are {fileNames}. 
    4. Each files have different columns. Here are the columns in each file. {arr} 
    5. Based on that, whenever you are reading the csv file, you should use the existing column from the csv you read. You are not allowed to create a column of a specific table to make your code works. All the visualization must come from related table and existing column of the table. Refer {arr} for the columns in each file.
    6. You should only provide python code which is use to show the visualization.Ensure the code is working perfectly without any error. Visualization should have title, label, x and y axis. 
    7. The visualization should be able to save as image. The image must be saved as a name of \"chart.png\". 
    8. When reading the csv into pandas DataFrame, add {folderPath} as the path and followed by whatever csv file to let the user to be able to run the code. The path should be like {folderPath}\\\"the csv file suits with requirement\".
    9. You should not provide any explanation or context of your code, only code is provided. You should not provide any code that is not related to the visualization. You should not provide any code that is not working. You should not provide any code that is not in python. You should not provide any code that is not related to the data that you are train on. You should not provide any code that is not related to the data visualization.
    """

    return systemContext

#Function that modify the system context

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

    response, encodedImage = chatWithLlama3(UUID, message)

    return response, encodedImage
    
def chatWithLlama3(UUID, message):
    
    # output = ollama.generate(
    #     model='llama3',
    #     prompt = message,
    #     system= systemContext,
    #     stream=True,      
    #     context= context,  
    # )

    msgs=[
        {"role": "system", "content": getSystemPrompt()},
        {"role": "user", "content": "draw me a bar chart of total orders based on customer id"},
        {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norders_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\Orders.csv\")\ntotal_orders = orders_df.groupby('CustomerID')['OrderID'].count().reset_index(name='Total Orders')\n\nplt.bar(total_orders['CustomerID'], total_orders['Total Orders'])\nplt.xlabel('Customer ID')\nplt.ylabel('Total Orders')\nplt.title('Total Orders by Customer ID')\nplt.savefig('chart.png')\n```"},
        {"role": "user", "content": "draw me a bar chart of total orders based on different product"},
        {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norder_details_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\OrderDetails.csv\")\n\n# Calculate total sales per product\norder_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']\nproduct_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()\n\n# Plot the total sales\nplt.figure(figsize=(10, 6))\nplt.bar(product_sales['ProductID'].astype(str), product_sales['TotalSales'], color='skyblue')\nplt.xlabel('Product ID')\nplt.ylabel('Total Sales')\nplt.title('Total Sales by Product')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.savefig('chart.png')\n```"},
        {"role": "user", "content": message},
    ]

    output = ollama.chat(
        model='llama3',
        messages = msgs,
        stream=True,
    )

    response = ""

    for chunk in output:
        print(chunk['message']['content'], end='', flush=True)
        response += chunk['message']['content']

    tr.transformResponse(response)

    time.sleep(5)# wait for the image to be generated

    image_file = open("chart.png", "rb")

    encodedImage = base64.b64encode(image_file.read()).decode('utf-8')

    toStoreJson = {
        "role": "AI",
        "content": encodedImage,
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file:
        data = json.load(file) 
        data["history"].append(toStoreJson)
        # data["context"] = toWriteContext

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file:
        json.dump(data, file, indent=4)
    return response, encodedImage

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
