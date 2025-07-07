import os
import uuid
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
    """
    A collection of methods that will be used to build
    our agent.
    """
    def __init__(self):
        self.llm = ChatOpenAI(model=os.getenv("MODEL_NAME"))

    @property
    def tools(self):
        """List of tools accesible to the LLM"""
        return [DuckDuckGoSearchResults(num_results=5, output_format="json")]

    def call_llm(self, state: AgentState) -> AgentState:
        """Send the messages from the state to LLM"""
        return {"messages": [self.llm.bind_tools(self.tools).invoke(state["messages"])]}

    def should_continue(self, state: AgentState) -> Literal["__end__", "tools"]:
        """Whether to continue the agent execution or stop it"""
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "__end__"

    def build_workflow(self):
        """Build the agent"""
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


class ChatHandler:
    """
    An interface for the Conversational Agent.

    Attributes:
        workflow: instance of the compiled agent
        thread_id (str): Session ID for Gradio WebApp
    """
    def __init__(self):
        self.workflow = Chatbot().build_workflow()
        self.thread_id = str(uuid.uuid4())

    def format_response(self, state: AgentState) -> List[OpenAIMessage]:
        """Reformat messages from LLM server to our own API server"""
        response = list()
        for message in state["messages"]:
            response.append({"role": message.type, "content": message.content})
        return response

    def chat_with_gradio(self, message: str, history: List) -> str:
        """Method to be used by `gradio.ChatInterface` for the webapp"""
        # add message to chat history
        messages = history + [{"role": "user", "content": message}]

        # pass agent
        response: AgentState = self.workflow.invoke(
            {"messages": messages}, config={"thread_id": self.thread_id}
        )

        # get last message
        return response["messages"][-1].content

    async def chat_with_api(
        self, thread_id: str, messages: List[OpenAIMessage]
    ) -> List[OpenAIMessage]:
        """Method to be used by FastAPI"""
        response: AgentState = await self.workflow.ainvoke(
            {"messages": messages}, config={"configurable": {"thread_id": thread_id}}
        )

        return self.format_response(response)
