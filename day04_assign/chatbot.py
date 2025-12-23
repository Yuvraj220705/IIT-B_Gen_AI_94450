import streamlit as st
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Chatbot")
st.title("Ruby Chatbot")

st.session_state.setdefault("chats", {"Chat 1": []})
st.session_state.setdefault("current_chat", "Chat 1")
st.session_state.setdefault("edit_index", None)
st.session_state.setdefault("edit_text", "")
st.session_state.setdefault("awaiting_reply", False)

#API_callings
def call_groq(p):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": p}]},
        timeout=30,
    )
    return r.json()["choices"][0]["message"]["content"]

def call_gemini(p):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    r = requests.post(url, headers={"Content-Type": "application/json"},
        data=json.dumps({"contents": [{"parts": [{"text": p}]}]}), timeout=30)
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def call_phi4(p):
    r = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={"Authorization": "Bearer dummy-key","Content-Type": "application/json"},
        data=json.dumps({"model": "microsoft/phi-4-mini-reasoning","messages": [{"role": "user","content": p}]}),
        timeout=30,
    )
    return r.json()["choices"][0]["message"]["content"]

def call_llama_local(p):
    r = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={"Authorization": "Bearer dummy-key","Content-Type": "application/json"},
        data=json.dumps({"model": "meta-llama-3-4b-mlp-pruned","messages": [{"role": "user","content": p}]}),
        timeout=30,
    )
    return r.json()["choices"][0]["message"]["content"]

def get_reply(prompt, model):
    return (
        call_groq(prompt) if model == "GROQ Model"
        else call_gemini(prompt) if model == "Gemini Model"
        else call_phi4(prompt) if model == "Phi-4 mini model"
        else call_llama_local(prompt)
    )

#sidebar
with st.sidebar:
    st.header("Options")
    model = st.radio(
        "Select Model",
        ["GROQ Model","Gemini Model","Phi-4 mini model","meta-llama-3-4b-mlp-pruned model"]
    )

    if st.button("New Chat"):
        name = f"Chat {len(st.session_state.chats)+1}"
        st.session_state.chats[name] = []
        st.session_state.current_chat = name

    st.divider()
    for chat in st.session_state.chats:
        if st.button(chat):
            st.session_state.current_chat = chat

messages = st.session_state.chats[st.session_state.current_chat]

#display-msg
for i, msg in enumerate(messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "user" and i == len(messages) - 2 and st.session_state.edit_index is None:
            if st.button("Edit Prompt", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.session_state.edit_text = msg["content"]
                st.rerun()

#edit_mode
if st.session_state.edit_index is not None:
    edited = st.text_area("Modify prompt", st.session_state.edit_text)
    c1, c2 = st.columns(2)
    if c1.button("Regenerate"):
        idx = st.session_state.edit_index
        messages[idx]["content"] = edited
        messages.pop(idx + 1)
        reply = get_reply(edited, model)
        messages.insert(idx + 1, {"role": "assistant","content": reply})
        st.session_state.edit_index = None
        st.rerun()

    if c2.button("Cancel"):
        st.session_state.edit_index = None

#chat_input
user_input = st.chat_input("Say something...")
if user_input:
    messages.append({"role": "user","content": user_input})
    st.session_state.awaiting_reply = True
    st.rerun()

#assistant_replay
if st.session_state.awaiting_reply:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_reply(messages[-1]["content"], model)
            st.markdown(reply)
    messages.append({"role": "assistant","content": reply})
    st.session_state.awaiting_reply = False
    st.rerun()
