# for responses
# TODO: add responses

from df_engine.core import Actor, Context
from helper_functions.requesting import weather_forecast_request


def basic_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    data = weather_forecast_request()
    degree = u'\N{DEGREE SIGN}'
    forecast = f"The temperature in {data['loc']} is {data['temp']}{degree}C. It feels like " \
               f"{data['feels-like']}{degree}C.\nDo you want to get more information?"
    return forecast


def extra_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    data = weather_forecast_request(extra=True)
    forecast = f"Weather report: {data['report']}. The humidity level is {data['humidity']}% " \
               f"and the wind speed is {data['wind']} m/s."
    return forecast
