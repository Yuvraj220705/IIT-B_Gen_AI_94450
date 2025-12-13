import requests

API_KEY = 'f2307613d404c0782b47a3a3edd99ac2'  # Replace with your real key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"   # for °C temperature
}

response = requests.get(BASE_URL, params=params)
data = response.json()

if data["cod"] == 200:
    print(f"\nWeather in {data['name']}:")
    print("Temperature:", data["main"]["temp"], "°C")
    print("Feels like:", data["main"]["feels_like"], "°C")
    print("Humidity:", data["main"]["humidity"], "%")
    print("Description:", data["weather"][0]["description"])
else:
    print("City not found! Please enter a valid city name.")
