import os
import time
import requests
import json

api_key = "shrya"
url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"

}

while True:
    user_input = input("ask anything:")
    if user_input.lower() == "exit":
        break

    req_data = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages" : [
            {
            "role": "user",
            "content": user_input
        }
        ]
    }

    time1 = time.perf_counter()
    
    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    time2 = time.perf_counter()
    resp = response.json()
    print("Status:", response.status_code)  
    print(resp["choices"][0]["message"]["content"])
    

    print(f"Time required: {time2-time1:.2f} sec")