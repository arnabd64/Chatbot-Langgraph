import uuid
from typing import Annotated, List

import gradio
from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

from src.agent import ChatHandler
from src.schema import APIResponse, OpenAIMessage
from src.webapp import webapp

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Server is Running"


@app.get("/chat/id", response_class=PlainTextResponse)
async def generate_chat_id():
    return str(uuid.uuid4())


@app.post("/chat/{id}", response_model=APIResponse)
async def agentic_chat(
    id: str, messages: List[OpenAIMessage], handler: Annotated[ChatHandler, Depends()]
) -> APIResponse:
    return {"error": "false", "data": await handler.chat_with_api(id, messages)}


app = gradio.mount_gradio_app(app, webapp, "/app")
