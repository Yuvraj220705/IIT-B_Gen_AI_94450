from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
open_weather_api = os.getenv("OPEN_WEATHER_API")

@tool
def calculator(expression):
    """
    this calculator function is a highly trained calculator and can compute high end mathematics questions in seconds.
    it supports arithmetic operators 
    
    :param expression: str input arthithmetic expression
    :returns expression result as str
    """

    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: cant resolve the expression"
    
def get_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.   

    :param city: Description
    :
    """
    try:
        api_key = "OPEN_WEATHER_API"
        
        url = "https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    


    except:
        return "Error"
    
@tool
def read_file(filepath):
    """
    Docstring for read_file
    
    :param filepath: Description
    """
    filepath = r"C:\Users\Shree\Desktop\Gen_AI\IIT-B_Gen_AI_94450\Day06\demo\employees.csv"
    with open(filepath,'r') as file:
        text = file.read()
        return text
    
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider= "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = "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"

)

agent = create_agent(
            model=llm,
            tools=[
                calculator,
                get_weather,
                read_file
            ],

            system_prompt="You are a helpful assistant. Amswer in short"
    )

while True:
    user_input = input("user: ")
    if user_input == "exit":
        break
    result = agent.invoke({
        "messages": [
            {"role": "user" , "content": user_input}
        ]
    })
        
    llm_output = result["messages"][-1]
    print("AI:", llm_output.content)
 


    