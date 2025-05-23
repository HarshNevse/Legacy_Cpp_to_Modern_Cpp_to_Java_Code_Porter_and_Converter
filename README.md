# Legacy C++ to Modern C++ to Java Code Porter and Converter

A web-based application that intelligently converts C++ code to Java using AI-powered language models. The tool supports both legacy C++98 code (with automatic modernization to C++11+) and direct conversion from modern C++ to Java.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Video Demo](#video-demo)
- [API Endpoints](#api-endpoints)
- [Frontend Features](#frontend-features)

## Overview

This application provides a streamlined solution for developers who need to convert C++ code to Java. It handles the conversion process in two intelligent stages:

1. **Legacy C++98 → Modern C++11+**: Automatically modernizes legacy C++ code using contemporary language features
2. **Modern C++ → Java**: Converts modern C++ code to equivalent Java implementation

The tool uses advanced language models to ensure accurate, contextually-aware conversions while maintaining code logic and structure.

## Features

### Core Functionality
- **Two-Stage Conversion Pipeline**: Seamless conversion from legacy C++ to modern Java
- **AI-Powered Conversion**: Uses Groq's Llama3-70B model for intelligent code translation
- **Smart Code Detection**: Automatically handles different C++ standards and paradigms
- **Markdown Output**: Results displayed with syntax highlighting and formatting

### User Interface
- **Intuitive Navigation**: Tab-based interface for easy workflow management
- **Real-time Preview**: Instant visualization of conversion results
- **Copy to Clipboard**: One-click copying of generated code
- **Clear Functions**: Individual and bulk content clearing options
- **Responsive Design**: Works seamlessly across different screen sizes
- **Error Feedback**: Clear error messages and loading states

### Technical Features
- **Robust Error Handling**: Graceful handling of API failures and edge cases
- **Session Management**: Maintains conversion state throughout user session
- **Markdown Rendering**: Professional code presentation with marked.js
- **RESTful API**: Clean API design for easy integration

## Technology Stack

### Backend
- **Framework**: Flask (Python web framework)
- **AI/ML**: LangChain, LangGraph for LLM orchestration
- **Language Model**: Groq API with Llama3-70B-8192
- **HTTP Client**: Built-in Flask request handling

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with responsive design
- **Markdown**: marked.js for code rendering
- **Architecture**: Single-page application (SPA)

### Infrastructure
- **Deployment**: Flask development server (production-ready WSGI recommended)
- **API**: RESTful endpoints with JSON communication
- **Environment**: Environment variable configuration

## Project Structure

```
cpp-to-java-converter/
├── app.py                 # Main Flask application
├── prompt_templates.py    # LLM prompt templates
├── templates/
│   └── index.html        # Frontend application
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Installation

### Prerequisites
- Python 3.8+
- Groq API account and API key
- Modern web browser

## Configuration

### Environment Variables

Set your Groq API key as an environment variable:

```bash
# Linux/macOS
export GROQ_API_KEY="your_groq_api_key_here"

# Windows
set GROQ_API_KEY=your_groq_api_key_here
```

### Model Configuration

The application uses the following LLM settings (configurable in `app.py`):
- **Model**: llama3-70b-8192
- **Temperature**: 0.1 (for consistent results)
- **Max Tokens**: 800
- **Max Retries**: 2

### Conversion Workflow

#### For Legacy C++ Code:
1. Select "I have Legacy C++ code"
2. Paste your C++98 code in the input area
3. Click "Port to Modern C++" to modernize the code
4. Review the Modern C++ output
5. Click "Convert to Java" to generate Java code
6. Copy or download the final Java implementation

#### For Modern C++ Code:
1. Select "I have Modern C++ code"
2. Paste your modern C++ code in the input area
3. Click "Convert to Java" for direct conversion
4. Review and copy the generated Java code

### Navigation Features
- Use **Previous/Next** buttons to navigate between conversion stages
- **Dots indicator** shows current position in the workflow
- **Clear** buttons to reset individual sections or entire application
- **Copy** buttons for easy code sharing

## Video Demo



https://github.com/user-attachments/assets/04d62d9a-9baf-488f-954d-4b92c94b61cd



## API Endpoints

### POST /port_legacy_cpp
Converts Legacy C++ code to Modern C++.

**Request:**
```json
{
  "code": "your_legacy_cpp_code_here"
}
```

**Response:**
```json
{
  "status": "success",
  "modern_cpp_code_raw_output": "converted_modern_cpp_with_explanation"
}
```

### POST /convert_modern_cpp_to_java
Converts Modern C++ code to Java.

**Request:**
```json
{
  "code": "your_modern_cpp_code_here"
}
```

**Response:**
```json
{
  "status": "success",
  "java_code_raw_output": "converted_java_code_with_explanation"
}
```

## Frontend Features

### User Interface Components
- **Code Selection**: Radio buttons for choosing input type
- **Code Areas**: Dedicated sections for input, Modern C++, and Java output
- **Navigation Controls**: Intuitive workflow navigation
- **Action Buttons**: Context-aware conversion and utility buttons

### Interactive Elements
- **Dynamic Button States**: Buttons enable/disable based on content availability
- **Real-time Validation**: Input validation with user feedback
- **Loading States**: Visual indicators during API calls
- **Status Messages**: Success and error notifications

---

**Note**: This application requires a valid Groq API key for LLM functionality. Ensure you have appropriate API quotas and follow Groq's usage guidelines.

For questions, issues, or feature requests, please open an issue on GitHub.

## Author
Developed by Harsh, AI/ML Enthusiast.
