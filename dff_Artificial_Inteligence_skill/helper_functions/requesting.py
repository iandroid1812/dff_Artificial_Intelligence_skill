import requests

# API key for Open Weather service
api_key_ow = "7acc0460a154cd92d4d98acfe6831f97"
current_location = "Moscow"


def weather_forecast_request(extra=False) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={current_location}&units=metric&appid={api_key_ow}"
    response = requests.get(url)
    if response.status_code != 200:
        return dict()
    data = response.json()

    if extra:
        return {
            "report": data['weather'][0]['main'],
            "humidity": data['main']['humidity'],
            "wind": round(data['wind']['speed'])
        }

    return {
        "loc": current_location,
        "temp": round(data['main']['temp']),
        "feels-like": round(data['main']['feels_like'])
    }
