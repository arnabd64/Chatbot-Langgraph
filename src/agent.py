import os
from typing import List, Literal

import dotenv
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from src.schema import AgentState, OpenAIMessage

dotenv.load_dotenv()


class Chatbot:

    def __init__(self):
        self.llm = ChatOpenAI(model=os.getenv("MODEL_NAME"))


    @property
    def tools(self):
        return [
            DuckDuckGoSearchResults(
                num_results = 5,
                output_format = "json"
            )
        ]


    def call_llm(self, state: AgentState) -> AgentState:
        return {
            "messages": [
                self.llm
                .bind_tools(self.tools)
                .invoke(state["messages"])
            ]
        }
    

    def should_continue(self, state: AgentState) -> Literal["__end__", "tools"]:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "__end__"
    

    def build_workflow(self):
        return (
            StateGraph(AgentState)
            .add_node("LLM", self.call_llm)
            .add_node("tools", ToolNode(self.tools))
            .add_edge("__start__", "LLM")
            .add_edge("LLM", "__end__")
            .add_edge("tools", "LLM")
            .add_conditional_edges("LLM", self.should_continue)
            .compile(checkpointer=InMemorySaver())
        )
    

    def format_response(self, state: AgentState) -> List[OpenAIMessage]:
        response = list()
        for message in state["messages"]:
            response.append({
                "role": message.type,
                "content": message.content
            })
        return response
