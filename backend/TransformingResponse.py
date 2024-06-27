import re
import subprocess

def transformResponse(response): # Function to transfrom response from AI model to runnable python code
    # print("response: ",response)
    pattern = r'```(?:python)?\s*(.*?)\s*```' # Regular expression pattern to extract code blocks
    code_blocks = re.findall(pattern, response, re.DOTALL) # Extract code blocks from response
    # print("code_blocks: ",code_blocks)
    generated_codes = "\n".join(code_blocks) # Join code blocks

    # print("generated code: ",generated_codes)
    # Step 2: Write the output to a Python file
    if generated_codes.strip(): # Check if code was generated
        # print(generated_codes)
        with open("generated_code.py", "w") as file: # Open a Python file
            file.write(generated_codes) # Write the generated code to the file

        # For executing the Python file using subprocess
        subprocess.run(["python", "generated_code.py"]) # Execute the Python file
    else:
        print("No code was generated.") # Print message if no code was generated