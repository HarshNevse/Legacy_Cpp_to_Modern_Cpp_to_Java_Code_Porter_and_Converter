# app.py
import getpass
import os
import json # To parse Langchain output potentially

# --- Keep LLM Setup and Core Logic ---
# Assume prompt_templates.py exists with porting_template and converting_template
# Assume Langchain/Langgraph setup is correct in the script
os.environ["GROQ_API_KEY"] = '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'
# Check/get Groq API key
#if "GROQ_API_KEY" not in os.environ:
    # In a web app, you might handle this differently,
    # maybe load from a config file or environment variable set on the server.
    # Using getpass is not suitable for a web server.
    # For demonstration, we'll assume it's set in the environment before running.
    #os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    #print("WARNING: GROQ_API_KEY not found in environment variables. Conversion will fail unless set.", flush=True)
    # As a placeholder for local testing, you might uncomment the getpass line
    # or load from a file, but be cautious with secrets in web apps.

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent # Assuming this is the right way based on script

# Assume prompt_templates.py is in the same directory
from prompt_templates import porting_template, conversion_template


# Initialize model and agents ONCE
# Need to handle potential API key error here or where Flask app starts
try:
    model = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.1,
        max_tokens=800,
        timeout=None,
        max_retries=2,
    )
    # Ensure agents are created using the actual templates and model
    porting_agent = create_react_agent(model=model, tools=[], prompt=porting_template)
    converting_agent = create_react_agent(model=model, tools=[], prompt=conversion_template)
    llm_setup_ok = True
except Exception as e:
    print(f"Error initializing LLM or agents: {e}", flush=True)
    llm_setup_ok = False
    # Create dummy agents if setup fails, so the app can still run (but won't convert)
    class DummyAgent:
        def invoke(self, input):
            print(f"LLM setup failed, using dummy agent. Input: {input}", flush=True)
            return {'messages': [{'content': 'Error: LLM setup failed. Cannot convert code.'}]}
    porting_agent = DummyAgent()
    converting_agent = DummyAgent()


# --- Conversion Functions (modified slightly for potential error handling) ---

def legacy_cpp_to_modern_cpp(legacy_cpp_code: str) -> dict:
    print('---'*15, flush=True)
    print('Porting legacy cpp code...', flush=True)
    print('---'*15, flush=True)
    if not llm_setup_ok:
         return {"modern_cpp_code": "", "explanation": "", "status": "error", "message": "LLM setup failed. Conversion not possible."}
    try:
        # Langchain Agent input structure: {'messages': user_input}
        r1 = porting_agent.invoke(input={'messages': legacy_cpp_code})
        print('Legacy cpp successfully ported.', flush=True)
        # Assuming the agent's response format is consistent
        # It should ideally follow the template structure
        # Need to parse r1 to get the code and explanation based on the template format
        # The user's script just returned the last message content
        # Let's try to extract based on the template structure if possible, or just return raw for now
        output_content = r1['messages'][-1].content
        # A robust app would parse output_content based on the template markdown sections (```cpp, [Explanation])
        # For now, return the raw output string. Frontend will need to parse it.
        return {"modern_cpp_code_raw_output": output_content, "status": "success"}
    except Exception as e:
        print(f"Error during porting: {e}", flush=True)
        return {"modern_cpp_code_raw_output": "", "status": "error", "message": str(e)}


def modern_cpp_to_java(modern_cpp_code: str) -> dict:
    print('---'*15, flush=True)
    print('Converting modern cpp code to java...', flush=True)
    print('---'*15, flush=True)
    if not llm_setup_ok:
         return {"java_code": "", "explanation": "", "status": "error", "message": "LLM setup failed. Conversion not possible."}
    try:
        # Langchain Agent input structure: {'messages': user_input}
        r1 = converting_agent.invoke(input={'messages': modern_cpp_code})
        print('Modern cpp successfully converted to java.', flush=True)
        # Assuming the agent's response format is consistent
        # It should ideally follow the template structure
        # Need to parse r1 to get the code and explanation based on the template format
        # Let's try to extract based on the template structure if possible, or just return raw for now
        output_content = r1['messages'][-1].content
        # A robust app would parse output_content based on the template markdown sections (```java, [Optional Explanation])
        # For now, return the raw output string. Frontend will need to parse it.
        return {"java_code_raw_output": output_content, "status": "success"}
    except Exception as e:
        print(f"Error during conversion: {e}", flush=True)
        return {"java_code_raw_output": "", "status": "error", "message": str(e)}

# --- Flask App Setup ---
from flask import Flask, request, jsonify, render_template # Need render_template if serving HTML

app = Flask(__name__)

# --- Flask Routes ---

# Basic route for the homepage (optional, might serve an HTML form)
# If you have an HTML file (e.g., index.html) in a 'templates' folder,
# you could use render_template('index.html')
@app.route('/')
def index():
    # For simplicity, just return a message or a basic form structure placeholder
    return render_template("index.html")
    # Or, if you create templates/index.html:
    # return render_template('index.html')


# Route to handle the 'Port' button click (Legacy C++ -> Modern C++)
@app.route('/port_legacy_cpp', methods=['POST'])
def port_legacy_cpp_route():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 415 # Unsupported Media Type

    data = request.get_json()
    legacy_cpp_code = data.get('code', '')

    if not legacy_cpp_code:
        return jsonify({"status": "error", "message": "No code provided"}), 400 # Bad Request

    # Call the core conversion function
    result = legacy_cpp_to_modern_cpp(legacy_cpp_code)

    # Return the result as JSON
    return jsonify(result)


# Route to handle the 'Convert' button click (Modern C++ -> Java)
@app.route('/convert_modern_cpp_to_java', methods=['POST'])
def convert_modern_cpp_to_java_route():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 415 # Unsupported Media Type

    data = request.get_json()
    modern_cpp_code = data.get('code', '')

    if not modern_cpp_code:
        return jsonify({"status": "error", "message": "No code provided"}), 400 # Bad Request

    # Call the core conversion function
    result = modern_cpp_to_java(modern_cpp_code)

    # Return the result as JSON
    return jsonify(result)


# --- Running the App ---
# This part is for development/testing.
# For production, use a production-ready WSGI server like Gunicorn or uWSGI.
if __name__ == '__main__':
    # Ensure the API key is set before running, or handle the error gracefully
    if 'GROQ_API_KEY' not in os.environ and not llm_setup_ok:
         print("\n!!! Flask app cannot start because GROQ_API_KEY is not set and LLM setup failed. Please set the environment variable. !!!\n")
    else:
        # debug=True is useful for development, automatically reloads on code changes
        # In production, set debug=False
        print("\n--- Flask app starting ---", flush=True)
        print("LLM Setup Status:", "OK" if llm_setup_ok else "FAILED", flush=True)
        print("Access endpoints via POST requests to /port_legacy_cpp and /convert_modern_cpp_to_java", flush=True)
        print("---"*15, flush=True)
        app.run(debug=True, use_reloader=False) # Runs on http://127.0.0.1:5000/ by default