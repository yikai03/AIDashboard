import re
import subprocess

# Basically can use pylint to check code quality, also capture syntax error
# For runtime error, can use try except block to capture runtime error

def parse_pylint_output(pylint_output): # Function to parse the AI output through pylint
    error_types = { # Dictionary to map error types
        'C': 'Convention', # Convention
        'R': 'Refactor', # Refactor
        'W': 'Warning', # Warning
        'E': 'Error', # Error
        'F': 'Fatal' # Fatal
    }
    
    syntaxErrorCheckingResult = { # Dictionary to store the result of syntax error checking
        'Convention': [], # Convention
        'Refactor': [], # Refactor 
        'Warning': [], # Warning
        'Error': [], # Error
        'Fatal': [] # Fatal
    }
    
    for line in pylint_output.splitlines(): # Loop through each line in the pylint output
        match = re.match(r'^(.*?):(\d+):(\d+): ([CRWEF])\d+: (.*)', line) # Regular expression to match the error message
        if match: # If match is found
            error_type = error_types.get(match.group(4), 'Unknown') # Get the error type
            syntaxErrorCheckingResult[error_type].append(line) # Append the error message to the corresponding error type

    if(syntaxErrorCheckingResult['Error'] == []): # Check if there are any errors
        nothingError = "No error found" # Set nothingError to "No error found"
    else: # If there are errors
        nothingError = "Error found" # Set nothingError to "Error found"

    if(syntaxErrorCheckingResult['Fatal'] == []): # Check if there are any fatal
        nothingFatal = "No fatal found" # Set nothingFatal to "No fatal found"
    else: # If there are fatal
        nothingFatal = "Fatal found" # Set nothingFatal to "Fatal found"
    
    return syntaxErrorCheckingResult, nothingError, nothingFatal # Return the result of syntax error checking


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

        syntaxErrorChecking = subprocess.run(['pylint', "generated_code.py"], capture_output=True, text=True) # Run pylint on the generated code

        syntaxErrorCheckingResult, nothingError, nothingFatal = parse_pylint_output(syntaxErrorChecking.stdout) # Parse the pylint output

        try: # Try to execute the generated code
            exec(generated_codes, {}) # Execute the generated code
            runtimeError = "No runtime errors" # Set runtime_error to "No runtime errors."
        except Exception as e: # Exception handling
            runtimeError = str(e) # Set runtime_error to the error message

        return syntaxErrorCheckingResult, nothingError, nothingFatal, runtimeError # Return the generated code
    else:
        print("No code was generated. Indicates that AI provide empty code") # Print message if no code was generated