from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def calculator(expression):

    
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. Give me only answer not all description. dont give any of english text just answer.
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """


    

    
    result = eval(expression)
    return str(result)
   



llm = init_chat_model(
    model="meta-llama-3.1-8b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key",

)

agent = create_agent(
    model= llm,
    tools=[
        calculator

    ],

    system_prompt= "You are a helpful assistant. Amswer in short "
)

while True:
    user_input = input("User:")
    if user_input == "exit":
        break
    result = agent.invoke({
        "messages":
        [
            {"role": "user", "content": user_input}
        ]
    })

    llm_output = result["messages"] [-1]
    print("AI:", llm_output.content)

    

 

