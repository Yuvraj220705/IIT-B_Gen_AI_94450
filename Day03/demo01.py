import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("f2307613d404c0782b47a3a3edd99ac2")
url = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")

response = requests.get(url)
weather = response.json()
print(weather)