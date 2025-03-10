import requests

def get_weather():
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    params = {
        'dataType': 'rhrread',
        'lang': 'en',
        'v': '1'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        
        # Check if temperature, weather status, and humidity data exist
        if 'temperature' in weather_data and 'icon' in weather_data and 'humidity' in weather_data:
            print(f"{'Location':<30} {'Temperature (°C)':<20} {'Weather':<15} {'Humidity (%)'}")
            print("-" * 70)
            
            # Iterate over temperature data and format the output
            for temp in weather_data['temperature']['data']:
                location = temp['place']
                temperature = temp['value']
                
                # Get weather status
                weather_icon = weather_data['icon'][0]  # Get the first weather icon
                weather_desc = get_weather_description(weather_icon)
                
                # Get humidity data
                humidity = next((h['value'] for h in weather_data['humidity']['data'] if h['place'] == location), "N/A")
                
                print(f"{location:<30} {temperature:<20} {weather_desc:<15} {humidity}")
        else:
            print("No complete weather data available.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def get_weather_description(icon):
    # Return weather description based on icon number
    weather_descriptions = {
        0: "Fine",
        1: "Fine",
        2: "Cloudy",
        3: "Overcast",
        8: "Rain",
        9: "Rain",
        10: "Thunderstorm",
        11: "Fog",
        12: "Snow",
        # Add other statuses as needed
    }
    return weather_descriptions.get(icon, "Unknown")

get_weather()
