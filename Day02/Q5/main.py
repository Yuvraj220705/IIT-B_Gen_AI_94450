from services.weather_services import get_weather

API_KEY = 'f2307613d404c0782b47a3a3edd99ac2'

def main():
    city = input("Enter city name: ")
    data = get_weather(city, API_KEY)

    if data.get("cod") == 200:
        print(f"\nWeather in {data['name']}:")
        print("Temperature:", data["main"]["temp"], "°C")
        print("Humidity:", data["main"]["humidity"], "%")
        print("Description:", data["weather"][0]["description"])
    else:
        print("City not found!")

if __name__ == "__main__":
    main()
