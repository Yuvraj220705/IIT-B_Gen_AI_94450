from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

llm = init_chat_model(
    model = "meta-llama-3.1-8b-instruct",
    model_provider= "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "dummy-key"


)

conversation =[]

agent = create_agent(
    model = llm,
    tools=[],
    system_prompt = "you are very very talkative  assistant"
)

while True:
    user_input = input("User:")
    if user_input == "exit":
        break
    conversation.append({"role": "user", "content": user_input})

    #user_input = ("role" : "user" , "content" : user_input)

    result=agent.invoke({"messages" : conversation})
    ai_msg = result['messages'][-1]
    #print(result[ai_msg])
    print("AI:", ai_msg)
    print(result)
    conversation = result['messages']





