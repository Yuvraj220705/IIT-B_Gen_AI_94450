import os
import requests
import json
from dotenv import load_dotenv
import time



api_key = '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'
url = "https://api.groq.com/openai/v1/chat/completions"
print(api_key)
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

while True:
    user_input = input("ask anything:")
    if user_input.lower() == "exit":
        break
    req_data = {

        "model" : "llama-3.3-70b-versatile",
        "messages" : [
            {
                "role" : "user",
                "content" : user_input
            }

        ]


    }

    time1 = time.perf_counter()
    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    time2 = time.perf_counter()
    print("Status:", response.status_code)
    # print(response.json())
    resp = response.json()
    print(resp["choices"][0]["message"]["content"])
    print(f"Time required: {time2-time1:.2f} sec")