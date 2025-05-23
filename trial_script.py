# app.py
import getpass
import os
import json 

if 'GROQ_API_KEY' not in os.environ:
    os.environ["GROQ_API_KEY"] = input("Please enter your Groq API key: ")


from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent 

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

    porting_agent = create_react_agent(model=model, tools=[], prompt=porting_template)
    converting_agent = create_react_agent(model=model, tools=[], prompt=conversion_template)
    llm_setup_ok = True
except Exception as e:
    print(f"Error initializing LLM or agents: {e}", flush=True)
    llm_setup_ok = False


# --- Conversion Functions ---

def legacy_cpp_to_modern_cpp(legacy_cpp_code: str) -> dict:
    print('---'*15, flush=True)
    print('Porting legacy cpp code...', flush=True)
    print('---'*15, flush=True)
    if not llm_setup_ok:
         return {"modern_cpp_code": "", "explanation": "", "status": "error", "message": "LLM setup failed. Conversion not possible."}
    try:
        r1 = porting_agent.invoke(input={'messages': legacy_cpp_code})
        print('Legacy cpp successfully ported.', flush=True)
       
        output_content = r1['messages'][-1].content
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
        r1 = converting_agent.invoke(input={'messages': modern_cpp_code})
        print('Modern cpp successfully converted to java.', flush=True)
       
        output_content = r1['messages'][-1].content
        return {"java_code_raw_output": output_content, "status": "success"}
    except Exception as e:
        print(f"Error during conversion: {e}", flush=True)
        return {"java_code_raw_output": "", "status": "error", "message": str(e)}

# --- Flask App Setup ---
from flask import Flask, request, jsonify, render_template 

app = Flask(__name__)

# --- Flask Routes ---


@app.route('/')
def index():
    return render_template("index.html")


# Route to handle the 'Port' button click (Legacy C++ -> Modern C++)
@app.route('/port_legacy_cpp', methods=['POST'])
def port_legacy_cpp_route():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 415 # Unsupported Media Type

    data = request.get_json()
    legacy_cpp_code = data.get('code', '')

    if not legacy_cpp_code:
        return jsonify({"status": "error", "message": "No code provided"}), 400 # Bad Request

    # core conversion function
    result = legacy_cpp_to_modern_cpp(legacy_cpp_code)

    # result as JSON
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

    # core conversion function
    result = modern_cpp_to_java(modern_cpp_code)

    # result as JSON
    return jsonify(result)


# --- Running the App ---
if __name__ == '__main__':
    if 'GROQ_API_KEY' not in os.environ and not llm_setup_ok:
         print("\n!!! Flask app cannot start because GROQ_API_KEY is not set and LLM setup failed. Please set the environment variable. !!!\n")
    else:
        print("\n--- Flask app starting ---", flush=True)
        print("LLM Setup Status:", "OK" if llm_setup_ok else "FAILED", flush=True)
        print("Access endpoints via POST requests to /port_legacy_cpp and /convert_modern_cpp_to_java", flush=True)
        print("---"*15, flush=True)
        app.run(debug=True, use_reloader=False) # runs on http://127.0.0.1:5000/ by default
