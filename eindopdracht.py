import os
from dotenv import load_dotenv
import requests
import datetime

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment
api_Key = os.getenv("API")

if api_Key is None:
    print("API key not found. Please check your .env file.")
    exit(1)

def get_Weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_Key}&units=metric"
    weather_data = get_data_from_api(url)

    # Check for a valid response
    if weather_data:
        weather_info = [
            f"City: {weather_data['name']}",
            f"Temperature: {weather_data['main']['temp']}°C",
            f"Feels Like: {weather_data['main']['feels_like']}°C",
            f"Humidity: {weather_data['main']['humidity']}%",
            f"Weather: {weather_data['weather'][0]['description']}",
            f"Wind Speed: {weather_data['wind']['speed']} m/s"
        ]
        print_info(weather_info)
    else:
        print("Error fetching weather data:", weather_data.get("message", "Unknown error"))


def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_Key}&units=metric"
    forecast_data = get_data_from_api(url)

    if forecast_data:
        for forecast in forecast_data['list'][:5]:
            forecast_info = [
                f"Forecast for {city}: {forecast['dt_txt']}",
                f"Temperature: {forecast['main']['temp']}°C",
                f"Feels Like: {forecast['main']['feels_like']}°C",
                f"Humidity: {forecast['main']['humidity']}%",
                f"Weather: {forecast['weather'][0]['description']}",
                f"Wind Speed: {forecast['wind']['speed']} m/s",
                "-" * 40
            ]
            print_info(forecast_info)
    else:
        print("Error fetching forecast data:", forecast_data.get("message", "Unknown error"))


def get_Airpollution(city):
    location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_Key}"
    location_data = get_data_from_api(location_url)

    if location_data:
        lat = location_data[0]["lat"]
        lon = location_data[0]["lon"]

        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_Key}"
        airpollution_data = get_data_from_api(pollution_url)

        if airpollution_data:
            timestamp = airpollution_data["list"][0]["dt"]
            readable_date = datetime.datetime.fromtimestamp(timestamp).strftime(
                '%Y-%m-%d %H:%M:%S')

            airpollution_info = [
                f"City: {city}",
                f"Current Date and Time: {readable_date}",
                f"Air Quality Index (AQI): {airpollution_data['list'][0]['main']['aqi']}",
                "\nComponents:",
                f"- Carbon Monoxide (CO): {airpollution_data['list'][0]['components']['co']} µg/m³",
                f"- Nitric Oxide (NO): {airpollution_data['list'][0]['components']['no']} µg/m³",
                f"- Nitrogen Dioxide (NO2): {airpollution_data['list'][0]['components']['no2']} µg/m³",
                f"- Ozone (O3): {airpollution_data['list'][0]['components']['o3']} µg/m³",
                f"- Sulfur Dioxide (SO2): {airpollution_data['list'][0]['components']['so2']} µg/m³",
                f"- Fine Particles (PM2.5): {airpollution_data['list'][0]['components']['pm2_5']} µg/m³",
                f"- Coarse Particles (PM10): {airpollution_data['list'][0]['components']['pm10']} µg/m³",
                f"- Ammonia (NH3): {airpollution_data['list'][0]['components']['nh3']} µg/m³"
            ]
            print_info(airpollution_info)
        else:
            print("Error fetching air pollution data:", airpollution_data.get("message", "Unknown error"))
    else:
        print("City not found or no results returned.")

def print_info(info_list):
    for item in info_list:
        print(item)

def get_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving data: {response.status_code} - {response.text}")
        return None

print("\nWelcome to the weather application!\n")
while True:

    chosen_City = input("Which city would you like to know the weather conditions for?\n")
    options = ["Current weather", "Weather forecast", "Air pollution"]
    for i in range(len(options)):
        print(str(i + 1) + ". " + options[i])

    chosen_Option = input("Which option do you want to choose?\n")

    if chosen_Option == "1":
        get_Weather(chosen_City)
    elif chosen_Option == "2":
        get_forecast(chosen_City)
    elif chosen_Option == "3":
        get_Airpollution(chosen_City)
    else:
        print("Invalid option, please try again.")

    restart = input("\nWould you like to enter a new city? (yes/no): ").strip().lower()
    if restart != 'yes':
        print("Thank you for using the weather application. Goodbye!")
        break
