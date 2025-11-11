import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, DuckDuckGoSearchRun, WikipediaQueryRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load env
load_dotenv(".env")

prompt = '''

You are a friendly and knowledgeable medical assistant named Luna. Answer all questions clearly, accurately, and in simple language. 
Provide explanations that are safe, non-harmful, and general; do not give specific medical prescriptions or personal medical advice. 
When possible, cite trustworthy sources. 
Use a helpful and compassionate tone.

Examples of questions you may receive:
- "What causes a sore throat?"
- "Is paracetamol safe for children?"
Always provide safe, clear, and informative answers.

'''

# Streamlit UI
st.title("🔍 AI Powered Medic")
st.divider()

with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = os.getenv("GROQ_API_KEY") or st.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.warning("Please enter the Groq API Key in the Sidebar")
    st.stop()

# Initialize model
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)

# Tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=200)
wiki_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=200)


tools = [
    WikipediaQueryRun(api_wrapper=wiki_wrapper),
    ArxivQueryRun(api_wrapper=arxiv_wrapper),
    DuckDuckGoSearchRun(name="Search"),
]

# Memory (summary-based to avoid infinite history growth)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
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

if "greeting_shown" not in st.session_state:
    greeting = agent.run(prompt)
    st.session_state.history.append({"role": "assistant", "content": greeting})
    st.session_state.greeting_shown = True  # mark greeting as shown


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