from dotenv import load_dotenv
import os
import google.generativeai as genai
import csv
import pandas as pd
import json
import time
import base64
import TransformingResponse as tr

load_dotenv()

GENAI_API_KEY = os.getenv('GENAI_API_KEY')

genai.configure(api_key=GENAI_API_KEY)
# response = model.generate_content("write me a story of a frontend developer in 200 words")
# print(response)

generation_config = {
  "temperature": 1,
  "top_p": 0.6,
  "top_k": 1,
  "max_output_tokens": 2000,
}


safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

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
    10. You should only use the csv file that are passed to you in this system instruction. You should not use any other csv file that are not in the system instruction.
    """

    return systemContext


########################################################


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

    response, encodedImage = chatWithGemini(UUID, message)

    return response, encodedImage
    
def chatWithGemini(UUID, message):
    
    # output = ollama.generate(
    #     model='llama3',
    #     prompt = message,
    #     system= systemContext,
    #     stream=True,      
    #     context= context,  
    # )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=getSystemPrompt(),
        safety_settings=safety_settings,
        generation_config=generation_config
    )

    msgs=[
        # {"role": "system", "content": getSystemPrompt()},
        {"role": "user", "content": "draw me a bar chart of total orders based on customer id"},
        {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norders_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\Orders.csv\")\ntotal_orders = orders_df.groupby('CustomerID')['OrderID'].count().reset_index(name='Total Orders')\n\nplt.bar(total_orders['CustomerID'], total_orders['Total Orders'])\nplt.xlabel('Customer ID')\nplt.ylabel('Total Orders')\nplt.title('Total Orders by Customer ID')\nplt.savefig('chart.png')\n```"},
        {"role": "user", "content": "draw me a bar chart of total orders based on different product"},
        {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norder_details_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\OrderDetails.csv\")\n\n# Calculate total sales per product\norder_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']\nproduct_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()\n\n# Plot the total sales\nplt.figure(figsize=(10, 6))\nplt.bar(product_sales['ProductID'].astype(str), product_sales['TotalSales'], color='skyblue')\nplt.xlabel('Product ID')\nplt.ylabel('Total Sales')\nplt.title('Total Sales by Product')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.savefig('chart.png')\n```"},
        {"role": "user", "content": message},
    ]

    msgsInGenerateContent=[
        # {"role": "system", "content": getSystemPrompt()},
        "input: draw me a bar chart of total orders based on customer id",
        "output: ```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norders_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\Orders.csv\")\ntotal_orders = orders_df.groupby('CustomerID')['OrderID'].count().reset_index(name='Total Orders')\n\nplt.bar(total_orders['CustomerID'], total_orders['Total Orders'])\nplt.xlabel('Customer ID')\nplt.ylabel('Total Orders')\nplt.title('Total Orders by Customer ID')\nplt.savefig('chart.png')\n```",
        "input: draw me a bar chart of total orders based on different product",
        "output: ```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norder_details_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\OrderDetails.csv\")\n\n# Calculate total sales per product\norder_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']\nproduct_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()\n\n# Plot the total sales\nplt.figure(figsize=(10, 6))\nplt.bar(product_sales['ProductID'].astype(str), product_sales['TotalSales'], color='skyblue')\nplt.xlabel('Product ID')\nplt.ylabel('Total Sales')\nplt.title('Total Sales by Product')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.savefig('chart.png')\n```",
    ]
    
    # chat = model.start_chat(history=msgs)

    # response = chat.send_message(message)

    prompt = f"""Here is the history of the correct version of code that you should provide: {msgsInGenerateContent}
    Here is the question that you should provide the code: {message}
    """

    response = model.generate_content(prompt, stream=True)

    result = "".join([str(chunk.text) for chunk in response])
    
    # print("Result: ", result)

    # response = model.generate_content(response['message']['content'], stream=True)

    # for chunk in output:
    #     print(chunk['message']['content'], end='', flush=True)
    #     response += chunk['message']['content']

    tr.transformResponse(result)

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
    return result, encodedImage