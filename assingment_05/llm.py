import streamlit as st
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Groq Chatbot")
st.title("Groq Chatbot (Turn-Based Context)")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

#Sidebar
st.sidebar.header("Settings")
context_turns = st.sidebar.slider(
    "Number of last conversation turns",
    1, 10, 3
)
st.sidebar.caption("1 turn = user + assistant")

#Session State
st.session_state.setdefault(
    "conversation",
    [{"role": "system", "content": "You are a helpful assistant."}]
)

#Show Chat
for msg in st.session_state.conversation:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

#User Input 
user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    #Context limiting 
    system_msg = st.session_state.conversation[0]
    recent = st.session_state.conversation[1:][-context_turns * 2:]
    context = [system_msg] + recent

    #LLM Call 
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(context).content
            st.write(response)

    st.session_state.conversation.append({"role": "assistant", "content": response})

    st.sidebar.write("Messages sent:", len(context))
