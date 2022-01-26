import random
from scenario.main import actor
from helper_functions.test_prepare import preparation
import run_interactive
random.seed(314)


def run_test():
    testing_dialog = preparation()
    ctx = {}
    for in_request, true_out_response in testing_dialog:
        _, ctx = run_interactive.turn_handler(in_request, ctx, actor, true_out_response=true_out_response)
    print("test passed")


if __name__ == "__main__":
    run_test()
