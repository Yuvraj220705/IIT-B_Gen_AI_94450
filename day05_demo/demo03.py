from langchain.chat_models import init_chat_model
import os

from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model



llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider= "openai",
    base_url= "https://api.groq.com/openai/v1",
    api_key= os.getenv("GROQ_API_key")

)

conversation = list()

while True:
    user_input = input("User: ")
    if user_input == "exit":
        break


    user_msg = {"role": "user", "content": user_input}
    conversation.append(user_msg)

    result = llm.invoke(conversation)
    print("AI : ", result.content)
    llm_msg = {"role": "assistant", "content": result.content}
    conversation.append(llm_msg)    
