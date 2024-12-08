import os
from dotenv import load_dotenv
import requests
import datetime

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("API")

if not API_KEY:
    print("API key not found. Please check your .env file.")
    exit(1)


def getDataFromApi(url):
    """Fetch data from the API with error handling."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


def getWeather(city):
    """Fetch current weather data for a given city."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    weather_data = getDataFromApi(url)

    if weather_data:
        print("\n--- Current Weather ---")
        print(f"City: {weather_data['name']}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Feels Like: {weather_data['main']['feels_like']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Weather: {weather_data['weather'][0]['description']}")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print("------------------------")
        return True
    else:
        print("City not found. Please check the city name and try again.")
        return False


def getForecast(city):
    """Fetch weather forecast for the next few days."""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    forecast_data = getDataFromApi(url)

    if forecast_data:
        print(f"\n--- Weather Forecast for {city} ---")
        for forecast in forecast_data['list'][:5]:
            print(f"\nDate and Time: {forecast['dt_txt']}")
            print(f"Temperature: {forecast['main']['temp']}°C")
            print(f"Feels Like: {forecast['main']['feels_like']}°C")
            print(f"Humidity: {forecast['main']['humidity']}%")
            print(f"Weather: {forecast['weather'][0]['description']}")
            print(f"Wind Speed: {forecast['wind']['speed']} m/s")
            print("------------------------------")
        return True
    else:
        print("City not found. Please check the city name and try again.")
        return False


def getAirPollution(city):
    """Fetch air pollution data for a given city."""
    location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    location_data = getDataFromApi(location_url)

    if location_data:
        lat = location_data[0]["lat"]
        lon = location_data[0]["lon"]

        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        air_pollution_data = getDataFromApi(pollution_url)

        if air_pollution_data:
            timestamp = air_pollution_data["list"][0]["dt"]
            readable_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            print(f"\n--- Air Pollution in {city} ---")
            print(f"Date and Time: {readable_date}")
            print(f"Air Quality Index (AQI): {air_pollution_data['list'][0]['main']['aqi']}")
            print("\nComponents:")
            print(f"- Carbon Monoxide (CO): {air_pollution_data['list'][0]['components']['co']} µg/m³")
            print(f"- Nitric Oxide (NO): {air_pollution_data['list'][0]['components']['no']} µg/m³")
            print(f"- Nitrogen Dioxide (NO2): {air_pollution_data['list'][0]['components']['no2']} µg/m³")
            print(f"- Ozone (O3): {air_pollution_data['list'][0]['components']['o3']} µg/m³")
            print(f"- Sulfur Dioxide (SO2): {air_pollution_data['list'][0]['components']['so2']} µg/m³")
            print(f"- Fine Particles (PM2.5): {air_pollution_data['list'][0]['components']['pm2_5']} µg/m³")
            print(f"- Coarse Particles (PM10): {air_pollution_data['list'][0]['components']['pm10']} µg/m³")
            print(f"- Ammonia (NH3): {air_pollution_data['list'][0]['components']['nh3']} µg/m³")
            print("---------------------------------")
            return True
        else:
            print("Error fetching air pollution data. Please try again later.")
            return False
    else:
        print("City not found. Please check the city name and try again.")
        return False


def printInfo(info_list):
    """Print a list of information to the console."""
    for item in info_list:
        print(item)


def getCityInput():
    """Prompt the user to enter a city name, and ensure it is valid."""
    while True:
        city = input("\nEnter the city name (or type 'exit' to quit): ").strip()
        if city.lower() == 'exit':
            print("Goodbye!")
            exit()
        if city:
            return city
        else:
            print("Please enter a valid city name.")


def mainMenu():
    """Display the main menu of the application."""
    options = ["Current weather", "Weather forecast", "Air pollution"]
    print("\n--- Welcome to the Weather Application ---\n")
    print("Select one of the options below:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("----------------------------------------")


def chooseOption():
    """Prompt the user to choose an option from the main menu."""
    while True:
        try:
            chosen_option = int(input("Which option would you like to choose? (1/2/3): "))
            if chosen_option in [1, 2, 3]:
                return chosen_option
            else:
                print("Invalid option. Please choose between 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")


def main():
    """The main loop of the program that leads the user through the options."""
    while True:
        mainMenu()  # Display the main menu
        chosen_option = chooseOption()  # Get the user's choice

        while True:
            chosen_city = getCityInput()  # Get the city from the user

            # Process the user's choice
            if chosen_option == 1:
                if getWeather(chosen_city):
                    break
            elif chosen_option == 2:
                if getForecast(chosen_city):
                    break
            elif chosen_option == 3:
                if getAirPollution(chosen_city):
                    break

        restart = input("\nWould you like to enter a new city? (yes/no): ").strip().lower()
        if restart != 'yes':
            print("Thank you for using the weather application. Goodbye!")
            break


# Start the application
if __name__ == "__main__":
    main()
