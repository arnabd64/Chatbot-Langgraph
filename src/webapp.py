"""
Source code for WebApp built using gradio library
"""

import gradio as gr

from src.agent import ChatHandler

webapp = gr.ChatInterface(
    fn=ChatHandler().chat_with_gradio,
    multimodal=False,
    type="messages",
    title="Langgraph Chatbot",
    analytics_enabled=True,
)
