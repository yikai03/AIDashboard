from dotenv import load_dotenv
import os
import google.generativeai as genai
import csv
import pandas as pd
import json
import time
import base64
import TransformingResponse as tr

load_dotenv() #Load the environment variables

GENAI_API_KEY = os.getenv('GENAI_API_KEY') #Get the API key from the environment variables

genai.configure(api_key=GENAI_API_KEY) #Configure the API key
# response = model.generate_content("write me a story of a frontend developer in 200 words")
# print(response)

generation_config = { #Initialize the generation configuration which will decide the AI's behavior
  "temperature": 1, #Set the temperature to 1 which means the AI will be more creative
  "top_p": 0.6, #Set the top_p to 0.6 which means the AI will be selecting words that have a probability of 0.6 to be the next word
  "top_k": 1,  #Set the top_k to 1 which means the AI will select the top 1 word that has the highest probability to be the next word
  "max_output_tokens": 2000, #Set the maximum output tokens to 2000 which means the AI will generate a maximum of 2000 tokens
}


safety_settings = [ #Initialize the safety settings which will decide the AI's safety level
  {
    "category": "HARM_CATEGORY_HARASSMENT", #Set the category to HARM_CATEGORY_HARASSMENT which means the AI will block harassment content
    "threshold": "BLOCK_MEDIUM_AND_ABOVE" #Set the threshold to BLOCK_MEDIUM_AND_ABOVE which means the AI will block medium and above harassment content
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH", #Set the category to HARM_CATEGORY_HATE_SPEECH which means the AI will block hate speech content
    "threshold": "BLOCK_MEDIUM_AND_ABOVE" #Set the threshold to BLOCK_MEDIUM_AND_ABOVE which means the AI will block medium and above hate speech contenet
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", #Set the category to HARM_CATEGORY_SEXUALLY_EXPLICIT which means the AI will block sexually explicit content
    "threshold": "BLOCK_MEDIUM_AND_ABOVE" #Set the threshold to BLOCK_MEDIUM_AND_ABOVE which means the AI will block medium and above sexually explicit content
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT", #Set the category to HARM_CATEGORY_DANGEROUS_CONTENT which means the AI will block dangerous content
    "threshold": "BLOCK_MEDIUM_AND_ABOVE" #Set the threshold to BLOCK_MEDIUM_AND_ABOVE which means the AI will block medium and above dangerous content 
  },
]

cwd = os.getcwd() #Get the current working directory
relativePathForHistory = "DataStorage\\AISessionHistory" #Set the relative path for the AI session history
folderPathForHistory = os.path.join(cwd, relativePathForHistory) #Set the folder path for the AI session history

def get_csv_column_names(file_path): #Function to get the column names of a CSV file
    with open(file_path, 'r', newline='') as file: #Open the CSV file
        reader = csv.reader(file) #Read the CSV file
        column_names = next(reader) #Read the first row
    return column_names #Return the column names

def getSystemPrompt(): #Function to get the system prompt
    relativePath = "TrainingTable" #Set the relative path for the training table
    folderPath = os.path.join(cwd, relativePath) #Set the folder path for the training table
    files = os.listdir(folderPath) #Get the list of files in the folder
    fileNames = [file for file in files if os.path.isfile(os.path.join(folderPath, file))] #Get the list of file names

    arr = [] #Initialize an empty array
    for file in fileNames: #Loop through the file names
        folderssPath = f"{folderPath}\\{file}" #Set the folder path for the file
        columns = get_csv_column_names(folderssPath) #Get the column names of the file 
        columns_str = ', '.join(columns) #Join the column names
        value = file + " have " + columns_str #Set the array value
        arr.append(value) #Append the value to the array

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
    """ #Set the system context

    return systemContext


########################################################


def newChat(UUID): #Function to start a new chat
    toWriteJson = { #Initialize the JSON object to write
        "id": UUID, #Set the ID to the user's UniqueUserID
        "history": [], #Initialize the history array
        "context": [], #Initialize the context array
    }
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as jsonFile: #Open the JSON file of the user's UniqueUserID
        json.dump(toWriteJson, jsonFile, indent=4) #Dump the JSON object to the file

def getUserMessage(UUID, message): #Function to get the user's message
    toStoreJson = { #Initialize the JSON object to store
        "role": "user", #Set the role to user
        "content": message, #Set the content to the user's message
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file: #Open the JSON file of the user's UniqueUserID
        data = json.load(file) #Load the JOSN data
        data["history"].append(toStoreJson) #Append the user's message to the history array
        
    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file: #Open the JSON file of the user's UniqueUserID
        json.dump(data, file, indent=4) #Dump the JSON data to the file

    response, encodedImage = chatWithGemini(UUID, message) #Get the response and the encoded image from the chat with Gemini

    return response, encodedImage #Return the response and the encoded image
    
def chatWithGemini(UUID, message): #Function to chat with Gemini

    model = genai.GenerativeModel( #Initialize the generative model
        model_name="gemini-1.5-flash", #Set the model name to gemini-1.5-flash 
        system_instruction=getSystemPrompt(), #Set the system instruction to the system prompt
        safety_settings=safety_settings, #Set the safety settings to the safe settings
        generation_config=generation_config #Set the generation configuration to the generation configuration
    )

    # msgs=[
    #     # {"role": "system", "content": getSystemPrompt()},
    #     {"role": "user", "content": "draw me a bar chart of total orders based on customer id"},
    #     {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norders_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\Orders.csv\")\ntotal_orders = orders_df.groupby('CustomerID')['OrderID'].count().reset_index(name='Total Orders')\n\nplt.bar(total_orders['CustomerID'], total_orders['Total Orders'])\nplt.xlabel('Customer ID')\nplt.ylabel('Total Orders')\nplt.title('Total Orders by Customer ID')\nplt.savefig('chart.png')\n```"},
    #     {"role": "user", "content": "draw me a bar chart of total orders based on different product"},
    #     {"role": "assistant", "content": "```\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\norder_details_df = pd.read_csv(\"C:\\\\Users\\\\Tomta\\\\Desktop\\\\AIDashboard\\\\aidashboard\\\\backend\\\\TrainingTable\\\\OrderDetails.csv\")\n\n# Calculate total sales per product\norder_details_df['TotalSales'] = order_details_df['Quantity'] * order_details_df['UnitPrice']\nproduct_sales = order_details_df.groupby('ProductID')['TotalSales'].sum().reset_index()\n\n# Plot the total sales\nplt.figure(figsize=(10, 6))\nplt.bar(product_sales['ProductID'].astype(str), product_sales['TotalSales'], color='skyblue')\nplt.xlabel('Product ID')\nplt.ylabel('Total Sales')\nplt.title('Total Sales by Product')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.savefig('chart.png')\n```"},
    #     {"role": "user", "content": message},
    # ]

    msgsInGenerateContent=[ #Initialize the messages in the generate content
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
    """ #Get the prompt and format it for accurate results

    response = model.generate_content(prompt, stream=True) #Generate the content with the prompt and store the output in the response

    result = "".join([str(chunk.text) for chunk in response]) #Join the chunks of the response to get the result

    tr.transformResponse(result) #Transform the response

    time.sleep(5)# wait for the image to be generated

    image_file = open("chart.png", "rb") #Open the image file

    encodedImage = base64.b64encode(image_file.read()).decode('utf-8') #Encode the image file

    toStoreJson = { #Initialize the JSON object to store
        "role": "AI", #Set the role to AI
        "content": encodedImage, #Set the content to the encoded image
    }

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "r") as file: #Open the JSON file of the user's UniqueUserID
        data = json.load(file) #Load the JSON data
        data["history"].append(toStoreJson) #Append the AI's response to the history array

    with open(os.path.join(folderPathForHistory, f"{UUID}.json"), "w") as file: #Open the JSON file of the user's UniqueUserID
        json.dump(data, file, indent=4) #Dump the JSON data to the file
    return result, encodedImage #Return the result and the encoded image