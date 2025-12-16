import streamlit as st
import time

st.title("Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    mode = st.selectbox("Mode", ["Upper", "Lower", "Toggle"])

def stream_reply(reply):
    for word in reply.split():
        yield word + " "
        time.sleep(0.3)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

msg = st.chat_input("Let's chat")

if msg:
    st.session_state.messages.append(
        {"role": "user", "content": msg}
    )
    with st.chat_message("user"):
        st.write(msg)

    if mode == "Upper":
        reply = msg.upper()
    elif mode == "Lower":
        reply = msg.lower()
    else:
        reply = msg.swapcase()

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write_stream(stream_reply(reply))
