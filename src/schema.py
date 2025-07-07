"""
Module for defining all the datastructures needed for the project.
"""

from typing import Annotated, List, Literal, TypedDict, Union

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Schema for the data that flows through the
    agent at every single execution.

    Attributes:
        messages (list): List of Langchain Messages that will be passed on the LLM
    """
    messages: Annotated[List[BaseMessage], add_messages]


class APIResponse(TypedDict):
    """
    Response Schema for the `chat` endpoint

    Attributes:
        error (bool): whether error was encountered
        data (str | list): error message or chat messages
    """
    error: Literal["true", "false"]
    data: Union[str, List]


class OpenAIMessage(TypedDict):
    """
    Schema for individual chat message which is OpenAI compatible

    Attributes:
        role (str): who has created the message
        content (str): Message body
    """
    role: Literal["human", "ai", "tool"]
    content: str
