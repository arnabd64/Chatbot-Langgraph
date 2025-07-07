# 🤖 Conversation Agent using Langgraph

## 📋 Overview

This project implements a conversational agent (chatbot) using **Langgraph**, a library built on top of LangChain for creating robust and stateful multi-turn applications. The agent maintains context across conversations and demonstrates core principles for building interactive AI assistants.

## 📋 Prerequisites

- 🐍 Python 3.8+
- 🔑 OpenAI API key (or compatible API provider)
- 📦 Git

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/arnabd64/Chatbot-Langgraph.git
cd Chatbot-Langgraph
```

### 2️⃣ Environment Setup

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY="your-openai-api-key-here"
MODEL_NAME="gpt-4o-mini"

# Optional - for OpenAI compatible providers
OPENAI_API_BASE=""

# Optional - for Langsmith tracing
LANGSMITH_TRACING=true
LANGSMITH_PROJECT="Langgraph"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="your-langsmith-api-key-here"
```

### 3️⃣ Installation Options

Choose one of the following methods:

#### 🐍 Option A: Using pip (Standard)

```bash
# Create and activate virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate     # Linux/macOS
# OR
.venv\Scripts\activate        # Windows

# Install dependencies
pip install -e .

# Run the server
python main.py
```

#### ⚡ Option B: Using uv (Recommended)

```bash
# Install dependencies
uv sync

# Run the server
uv run python main.py
```

#### 🐳 Option C: Using Dev Container

Requires Visual Studio Code with Dev Containers extension:

1. Open VS Code: `code .`
2. Press `F1` and search for "Dev Containers: Rebuild and Reopen in Dev Containers"
3. Run: `uv run python main.py`

### 4️⃣ Access the Application

- 🌐 **Web Interface**: Visit `http://localhost:8000/app`
- 📖 **API Documentation**: Visit `http://localhost:8000/docs`

## 🔧 API Usage

### 🆔 Generate Session ID

Each chat session requires a unique session ID:

```bash
curl -X GET "http://localhost:8000/chat/id" -H "accept: text/plain"
```

**Response:**
```
dbaed28e-cf61-457a-b034-2bd48ab5424a
```

### 💬 Send Messages

Send messages using the session ID:

```bash
curl -X POST "http://localhost:8000/chat/dbaed28e-cf61-457a-b034-2bd48ab5424a" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "role": "human",
      "content": "Hi"
    }
  ]'
```

**Response:**
```json
{
  "error": "false",
  "data": [
    {
      "role": "human",
      "content": "Hi"
    },
    {
      "role": "ai",
      "content": "Hello! How can I assist you today?"
    }
  ]
}
```

## 📝 Message Format

Each message is a JSON object with:
- `role`: Message sender ("system", "human", or "ai")
- `content`: Message text

## ✨ Features

- 🔄 **Stateful Conversations**: Maintains context across multiple turns
- 🛠️ **FastAPI Integration**: REST API for easy integration
- 🌐 **Web Interface**: Built-in chat interface
- 🔒 **Session Management**: Isolated chat sessions using UUIDs
- 🔧 **OpenAI Compatible**: Works with OpenAI and compatible providers
- 📊 **Langsmith Integration**: Optional tracing and monitoring

