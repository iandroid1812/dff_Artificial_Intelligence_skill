import random

from scenario.main import actor
from helper_functions.requesting import weather_forecast_request
import run_interactive

random.seed(314)

# testing
data = weather_forecast_request() | (weather_forecast_request(extra=True))
degree = u'\N{DEGREE SIGN}'

testing_dialog = [
    ("Hi",
     "Hello, I am your Home Assistant. How can I help?"
     ),
    ("Please, tell me about the weather.",
     f"The temperature in {data['loc']} is {data['temp']}{degree}C. It feels like {data['feels-like']}{degree}C." \
     "\nDo you want to get more information?"
     ),
    ("Ok",
     f"Weather report: {data['report']}. The humidity level is {data['humidity']}% " \
     f"and the wind speed is {data['wind']} m/s."
     ),
    ("Great, thank you!",
     "Glad I could help!"),
    ("", None), # end of convo 1
    ("HEY",
     "Hello, I am your Home Assistant. How can I help?"
     ),
    ("Whats the weather outside?",
     f"The temperature in {data['loc']} is {data['temp']}{degree}C. It feels like {data['feels-like']}{degree}C." \
     "\nDo you want to get more information?"
     ),
    ("Nope",
     "Ok, that's it for the weather then.")
]


def run_test():
    ctx = {}
    for in_request, true_out_response in testing_dialog:
        if (in_request == "") & (true_out_response is None):
            ctx = {} # resets the context for next convo
        _, ctx = run_interactive.turn_handler(in_request, ctx, actor, true_out_response=true_out_response)
    print("test passed")


if __name__ == "__main__":
    run_test()
