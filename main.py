"""
Run the `main.py` file to deploy the FastAPI web server
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        headers=[("X-Application", "Langgraph-Chatbot")],
    )
