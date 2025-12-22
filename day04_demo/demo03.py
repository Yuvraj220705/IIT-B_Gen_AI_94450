import requests
import json
import streamlit as st

st.title("My Chatbot")

api_key = "shrya"
url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

user_input = st.text_input("Ask anything:")

if user_input:
    req_data = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    response = requests.post(url, headers=headers, json=req_data)

    if response.status_code == 200:
        resp = response.json()
        with st.chat_message("assistant"):
            st.write(resp["choices"][0]["message"]["content"])

