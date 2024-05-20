import re
import subprocess

def transformResponse(response):
    pattern = r'```(?:python)?\s*(.*?)\s*```'
    code_blocks = re.findall(pattern, response.text, re.DOTALL)
    generated_codes = "\n".join(code_blocks)

    # Step 2: Write the output to a Python file
    if generated_codes.strip():
        # print(generated_codes)
        with open("generated_code.py", "w") as file:
            file.write(generated_codes)

        # For executing the Python file using subprocess
        subprocess.run(["python", "generated_code.py"])
    else:
        print("No code was generated.")