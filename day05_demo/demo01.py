import streamlit as st
from langchain_groq import ChatGroq

from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

#api_key = os.getenv("GROQ_API_key")
#llm = ChatGroq(model_name="llama-3.3-70b-versatile" , groq_api_key=api_key)
#print(llm.invoke("Hello").content)


llm_url = "http://127.0.0.1:1234/v1"
llm = ChatOpenAI(
    base_url=llm_url,
    model="llama-3.3-70b",
    api_key="dummy-key"

)
user_input = st.chat_input("say something:")
if user_input:
    '''st.write(user_input)
result = llm.invoke(user_input)
print(result.content)
result = llm.stream(user_input)
print(result)'''

result = llm.stream(user_input)
for chunk in result:
    st.write(chunk.content for chunk in result)


#print(result)
