import json
from dotenv import load_dotenv

from google import genai
from google.genai import types

import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def query_db(sql):
    pass

def run_command(command):
    result = os.system(command=command)
    return result
def write_file(input_data):
    try:
        filename = input_data.get("filename")
        content = input_data.get("content")

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        return f"✅ File '{filename}' written successfully."
    except Exception as e:
        return f"❌ Error writing file '{filename}': {str(e)}"
    
def edit_file(filename, patch_fn):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content = patch_fn(content) if callable(patch_fn) else patch_fn

        with open(filename, "w", encoding="utf-8") as f:
            f.write(updated_content)

        return f"{filename} updated successfully."
    except Exception as e:
        return f"Error editing {filename}: {str(e)}"

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading {filename}: {str(e)}"

avaiable_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
    "write_file": {
        "fn": write_file,
        "description": "Writes raw code to a given file. Input must be a dict with keys: filename and content."
    },
    "edit_file": {
        "fn": edit_file,
        "description": "Edits a given file by applying a patch or replacing it entirely"
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads and returns the content of a file"
    }

}

system_prompt = f"""
    You are an helpfull AI Assistant senior developer who is specialized in resolving user commands and files. Always consider windows 11 before running commands.
    In case an error is observed, analyze the error message and suggest a plan and fix step to retry the command.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.
    When you are writing code in any file, write it as raw unescaped code. Do NOT stringify, escape, or wrap it in any quotes or special characters. Just paste it exactly as it should appear in the file. DO NOT include extra backslashes or newlines unless they are part of actual code.


    Rules:
    - Always create a new folder for each project, give some meaningful name to the folder and go into that folder in windows 11.
    - Follow the Output JSON Format.
    - Strictly Do not include any markdown formatting like ```json. Only output raw JSON.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"
    }}
    {{
        "step": "action",
        "function": "write_file",
        "input": {{
            "filename": "index.html",
            "content": "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Simple ToDo App</title><link rel=\"stylesheet\" href=\"style.css\"></head><body><script src=\"script.js\"></script></body></html>"
        }}
    }}
    {{
        "step": "action",
        "function": "write_file",
        "input": {{
            "filename": "index.html",
            "content": "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Simple ToDo App</title><link rel=\"stylesheet\" href=\"style.css\"></head><body><script src=\"script.js\"></script></body></html>"
        }}
    }}
    {{ 
        "step": "plan", "content": "User wants to add dark theme toggle" 
    }}
    {{ 
        "step": "plan", "content": "We'll update style.css with dark mode styles and add toggle script in script.js" 
    }}
    {{ 
        "step": "action", "function": "edit_file", 
        "input": {{
            "filename": "script.js",
            "patch": "document.body.classList.toggle('dark');"
        }}
    }}



    Available Tools:
    - run_command: Takes a command as input to execute on system and returns ouput
    - write_file: Takes input as an object with "filename" and "content", writes raw code directly to a file.
    - edit_file: Takes filename and patch (or full replacement) and updates the file.
    - read_file: Takes filename and returns the content of the file.



    Example:
    User Query: Build an react vite applications and edit modify by features and run the project
    Output: {{{{ "step": "plan", "content": "the user is interested in editing the react application." }}}}
    Output: {{{{ "step": "plan", "content": "from available tool we can call run_command" }}}}
    Output: {{{{ "step": "action", "function": "run_command", "input": "npm run dev" }}}}
    Output: {{{{ "step": "observe", "output": "Files created successfully. Files edited successfully." }}}}
    Output: {{{{ "step": "output", "content": "File changed: App.tsx" }}}}

    Example:
    User Query: create folder or file named "component" and functionality of components. When using write_file, always send raw, unescaped code — do not format it as a string or escape quotes.

    Output: {{{{ "step": "plan", "content": "the user is interested creating new folder or file component which it want to use in App.tsx or main.ts." }}}}
    Output: {{{{ "step": "plan", "content": "from available tool use run_command to create component example.tsx and add given funcitonality into it." }}}}
    Output: {{{{ "step": "action", "function": "write_file", "input": "index.html" }}}}
    Output: {{{{ "step": "observe", "output": "Component created successfully. Componnet edited successfully." }}}}
    Output: {{{{ "step": "output", "content": "File changed: TodoList.tsx" }}}}

    Example:
    User Query: run "npm run dev"
    Output: {{{{ "step": "action", "function": "run_command", "input": "npm run dev" }}}}
    Output: {{{{ "step": "observe", "output": "❌ Command failed with error: npm ERR! missing script: dev" }}}}
    Output: {{{{ "step": "fix", "content": "It seems like 'dev' script is missing in package.json. You can add it or run a valid script like 'npm start'.", "function": "run_command", "input": "npm start" }}}}
"""


messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:

        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=json.dumps(messages)
        )

        start_index = response.text.find('{')
        end_index = response.text.rfind('}') + 1 
        cleaned_string = response.text[start_index:end_index]

        try:
            parsed_output = json.loads(cleaned_string)
            print("Parsed Output: ", parsed_output)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            parsed_output = {"step": "output", "content": "Something went wrong, please try again."}



        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })
        # If Gemini suggests a retry or fix
        if parsed_output.get("step") == "fix":
            print(f"💡 Suggested Fix: {parsed_output.get('content')}")
            user_input = input("⚙️ Do you want to apply this fix? (y/n): ")
            if user_input.lower() == 'y':
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({
                        "step": "action",
                        "function": parsed_output.get("function"),
                        "input": parsed_output.get("input")
                    })
                })
            else:
                print("❌ Skipping fix.")
                break
            continue

        if parsed_output.get("step") == "plan":
            print(f'🧠: {parsed_output.get("content")}')
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            tool = avaiable_tools.get(tool_name)
            if tool:
                tool_fn = tool.get("fn")

                if tool_name == "edit_file" and isinstance(tool_input, dict):
                    filename = tool_input.get("filename")
                    patch = tool_input.get("patch")

                    if filename is None or patch is None:
                        output = "Missing 'filename' or 'patch' in tool input."
                    else:
                        if callable(patch):
                            output = tool_fn(filename, patch)
                        else:
                            output = tool_fn(filename, lambda content: patch)
                else:
                    output = tool_fn(tool_input)

                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output": output }) })
                continue

        if parsed_output.get("step") == "output":
            print(f'🤖: {parsed_output.get("content")}')
            break