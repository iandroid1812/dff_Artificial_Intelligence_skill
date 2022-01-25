import requests
from decouple import config

# API key for Open Weather service
api_key = config('OPEN_WEATHER')
current_location = "Moscow"


def weather_forecast_request():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={current_location}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return dict()
    data = response.json()

    return {
        "loc": current_location,
        "temp": round(data['main']['temp']),
        "feels-like": round(data['main']['feels_like']),
        "report": data['weather'][0]['main'],
        "humidity": data['main']['humidity'],
        "wind": round(data['wind']['speed'])
     }
