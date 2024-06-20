import re
import subprocess

#_________________________________INTRODUCTION_______________________________________
# As we are using AI to generate Python code, we need to transform the response into runnable Python code. 
# Although we can ask the AI to generate Python code directly, it is better to transform the response into runnable Python code since AI might provide some unnecessary information.

def transformResponse(response): # Function to transform the response to Runnable Python Code
    # print("response: ",response)
    pattern = r'```(?:python)?\s*(.*?)\s*```' #Regular expression to get the code block
    code_blocks = re.findall(pattern, response, re.DOTALL) #Find all the code blocks in the response
    # print("code_blocks: ",code_blocks)
    generated_codes = "\n".join(code_blocks) #Join all the code blocks with newline

    print("generated code: ",generated_codes)
    # Step 2: Write the output to a Python file
    if generated_codes.strip(): #Check if the generated code is not empty
        # print(generated_codes)
        with open("generated_code.py", "w") as file: #Open the file in write mode
            file.write(generated_codes) #Write the generated code to the file

        subprocess.run(["python", "generated_code.py"]) #Run the Python file using subprocess
    else:
        print("No code was generated.")