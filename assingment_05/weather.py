import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Weather App")
st.title("Weather App with LLM Explanation")

# LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)

city = st.text_input("Enter city name")

if st.button("Get Weather") and city:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code != 200:
        st.error("Invalid city name")
    else:
        data = res.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        condition = data["weather"][0]["main"]

        st.subheader(f"Weather in {city.title()}")
        st.write(f"Temperature: {temp} °C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Wind Speed: {wind} m/s")
        st.write(f"Condition: {condition}")

        prompt = f"""
        Explain these weather conditions simply:

        City: {city}
        Temperature: {temp} °C
        Humidity: {humidity}%
        Wind Speed: {wind} m/s
        Condition: {condition}
        """

        explanation = llm.invoke(prompt).content

        st.subheader("Simple Explanation")
        st.write(explanation)
