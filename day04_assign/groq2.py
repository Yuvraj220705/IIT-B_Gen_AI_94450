import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.title("Multi-LLM Chatbot")

st.sidebar.title("Settings")
model_choice = st.sidebar.radio(
    "Choose LLM:",
    ["Groq", "LM Studio"]
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask something...")



def get_groq_response(user_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {('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')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def get_lmstudio_response(user_prompt):
    url = "http://127.0.0.1:1234/v1/chat/completions"
    data = {
        "model": "google/gemma-3-4b",
        "messages": [{"role": "user", "content": user_prompt}]
    }
    response = requests.post(url, json=data)
    return response.json()["choices"][0]["message"]["content"]

if user_input:
    if model_choice == "Groq":
        reply = get_groq_response(user_input)
    elif model_choice == "LM Studio":
        reply = get_lmstudio_response(user_input)
    
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)