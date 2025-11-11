import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.memory import ConversationSummaryMemory
import os
from dotenv import load_dotenv

# Load env
load_dotenv(".env")

# Streamlit UI
st.title("🔍 Search Engine: Powered by Agentic AI and It's Context Aware")

with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = os.getenv("GROQ_API_KEY") or st.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.warning("Please enter the Groq API Key in the Sidebar")
    st.stop()

# Initialize model
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

# Tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=200)

tools = [
    ArxivQueryRun(api_wrapper=arxiv_wrapper),
    DuckDuckGoSearchRun(name="Search"),
]

# Memory (summary-based to avoid infinite history growth)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )

# Agent with memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=st.session_state.memory,
    handle_parsing_errors=True,
    verbose=False,
)

# Chat history rendering (UI only, separate from LangChain memory)
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Your message"):
    # Show user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent response
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.run(user_input, callbacks=[st_cb])
        st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})