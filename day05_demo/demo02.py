import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

st.title("Langchain Chatbot")

llm = init_chat_model(
    model= "llama-3.3-70b-versatile",
    base_url= "https://api.groq.com/openai/v1",
    api_key= os.getenv("GROQ_API_key"),
    model_provider="openai"


)

user_input = st.chat_input("say something:")
if user_input:
    result = llm.stream(user_input)
    for chunk in result:
        st.write(chunk.content for chunk in result)