import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Langchain Chatbot")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_key"),
    model_provider="openai"
)

# ✅ initialize once
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ user input must be OUTSIDE the init block
user_input = st.chat_input("say something:")

if user_input:
    # append user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    # ✅ invoke ONLY after at least one message exists
    response = llm.invoke(st.session_state.chat_history)

    # show assistant message
    with st.chat_message("assistant"):
        st.markdown(response.content)

    # save assistant message
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response.content}
    )
