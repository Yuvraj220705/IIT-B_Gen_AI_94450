import streamlit as st
import os
import requests

st.title("Multi-LLM Chatbot")


st.sidebar.title("setting")
model_choice = st.sidebar.radio(
    "Choose LLM:",
    ["Groq", "LM Studio"]
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input}
    )
    
reply = f"you selected {model_choice}"
st.session_state.chat_history.append({"role": "assistant", "content": reply})

