import uuid
from typing import Annotated, List

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse

from src.agent import Chatbot
from src.schema import AgentState, APIResponse, OpenAIMessage

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return 


@app.get("/chat/id", response_class=PlainTextResponse)
async def generate_chat_id():
    return str(uuid.uuid4())


@app.post("/chat/{id}", response_model=APIResponse)
async def agentic_chat(id: str, messages: List[OpenAIMessage], chatbot: Annotated[Chatbot, Depends()]) -> APIResponse:
    # compile agent
    workflow = chatbot.build_workflow()

    # invoke agent
    response: AgentState = await workflow.ainvoke(
        {"messages": messages},
        config = {
            "configurable": {
                "thread_id": id
            }
        }
    )

    return {
        "error": "false",
        "data": chatbot.format_response(response)
    }
