from langchain.chat_models import init_chat_model
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider= "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_key")

)

conversation = [
    {"role": "user", "content": "You are a pro sqlite expert who helps user to solve their queries in sqlite database."},

]

csv_file = print("Enter the path of csv file:")
df = pd.read_csv('C:\\Users\\Shree\\Desktop\\Gen_AI\\IIT-B_Gen_AI_94450\\day05_demo\\employees.csv')
print("File Information:")
print(df.dtypes)

while True:
    user_input = input("Ask something about the csv file:")
    if user_input == "exit":
        break
    user_msg = {"role": "user", "content": user_input}
    conversation.append(user_msg)

    llm_output = f"""
    table name: data,
    table info : {df.dtypes}
    Question : {user_input}

    instruction: Write a SQL query for the above question. 
                dont give me more information just write me the query 
                


"""
    
    result = llm.invoke(llm_output)
    print(result.content)


