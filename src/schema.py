from typing import Annotated, List, Literal, TypedDict, Union

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


class APIResponse(TypedDict):
    error: Literal["true", "false"]
    data: Union[str, List]


class OpenAIMessage(TypedDict):
    role: Literal["human", "ai", "tool"]
    content: str

