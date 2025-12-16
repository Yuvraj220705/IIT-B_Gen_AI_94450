import streamlit as st
st.title("chat bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Say something")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

reply = user_input
st.session_state.messages.append({"role": "assistant", "content": reply})
with st.chat_message("assistant"):
    st.write(reply)

