import df_engine.conditions as cnd
import df_engine.labels as lbl
from df_engine.core import Actor
from df_engine.core.keywords import RESPONSE, TRANSITIONS, GLOBAL

import scenario.label as loc_lbl
import scenario.condition as loc_cnd
import scenario.response as rsp


plot = {
    # GLOBAL node so we can have transition to some specific nodes at any
    # point of the conversation, for example we can stop the conversation at any time
    GLOBAL: {
        TRANSITIONS: {
            ("service_flow", "stop_convo", 2.0): cnd.regexp(r'\bstop\b|\bStop\b|\bстоп\b|\bСтоп\b'),

            # takes us to the starting node if we say thanks/bye. in one of the nodes below,
            # (usually after successful execution of a command). Response is customized using
            # conditions in the rsp.main_response function
            ("service_flow", "start_node"): cnd.all(
                [cnd.any([loc_cnd.appreciate_condition, loc_cnd.goodbye_condition]),
                 cnd.has_last_labels(labels=[
                     ("weather_flow", "extra"),
                     ("light_flow", "light_execution"),
                     ("dim_flow", "dim_execution"),
                     ("climate_flow", "set_temperature"),
                     ("climate_flow", "heat_up"),
                     ("climate_flow", "cool_down"),
                     ("home_presence_flow", "lights_check"),
                     ("home_presence_flow", "floor_heat")
                 ])]
            ),
            ("service_flow", "start_node"): cnd.all(
                [loc_cnd.greeting_condition, loc_cnd.beginning_condition]
            )
        }
    },
    "service_flow": {
        "start_node": {
            RESPONSE: rsp.main_response,
            TRANSITIONS: {
                ("service_flow", "start_node", 2.5): loc_cnd.lang_condition,
                ("service_flow", "start_node"): loc_cnd.goodbye_condition,

                ("weather_flow", "basic"): loc_cnd.weather_condition,

                # option 1: user tells us to only turn on the light, but does not specify
                # the room --> we go and ask him what is the required room
                ("light_flow", "room"): loc_cnd.light_condition,

                # option 2: user tells us his intention to turn on/off the light and
                # tells us the room in the same sentence --> we go to the execution node
                ("light_flow", "light_execution", 1.1): cnd.all(
                    [loc_cnd.light_condition, loc_cnd.room_condition]),

                ("dim_flow", "room"): loc_cnd.dim_condition,
                ("dim_flow", "brightness", 1.1): cnd.all(
                    [loc_cnd.dim_condition, loc_cnd.room_condition, loc_cnd.dimmable_condition]),
                ("dim_flow", "not_available", 1.1): cnd.all(
                    [loc_cnd.dim_condition, loc_cnd.room_condition]),

                ("climate_flow", "room"): loc_cnd.setting_temp_condition,
                ("climate_flow", "set_temperature", 1.1): cnd.all(
                    [loc_cnd.setting_temp_condition, loc_cnd.room_condition]),
                ("climate_flow", "heat_up", 1.1): cnd.all([
                    loc_cnd.heating_condition, loc_cnd.room_condition]),
                ("climate_flow", "cool_down", 1.1): cnd.all([
                    loc_cnd.cooling_condition, loc_cnd.room_condition]),

                ("home_presence_flow", "going_away"): loc_cnd.away,
                ("home_presence_flow", "getting_in"): loc_cnd.coming,

                ("service_flow", "start_node", 2.0): loc_cnd.tts_check,
                ("service_flow", "Q&A", 1.2): loc_cnd.question_answer
            }
        },
        "fallback_node": {
            RESPONSE: rsp.fallback,
            TRANSITIONS: {
                # "lbl.previous()" did not have the required functionality, if the user made mistake
                # in his request more than once, and only after that he said that he wants to return
                # to the previous node it returned him back to the error message. What I wanted to do is to
                # return user to the node before the error occurred. That is why I created a custom label
                # called "previous_fallback()" in label.py file
                loc_lbl.previous_fallback(): loc_cnd.condition_yes,
                lbl.to_start(): loc_cnd.condition_no,
                lbl.repeat(): cnd.true()
            }
        },
        "stop_convo": {
            RESPONSE: rsp.convo_stopped,
            TRANSITIONS: {
                lbl.to_start(): cnd.regexp(r'\bstart\b|\bStart\b|\bначать\b|\bНачать\b'),
                # repeat until user says start
                lbl.repeat(): cnd.true()
            }
        },
        "Q&A": {
            RESPONSE: rsp.questioning,
            TRANSITIONS: {
                lbl.repeat(): cnd.true()
            }
        }
    },
    "weather_flow": {
        "basic": {
            RESPONSE: rsp.basic_weather_response,
            TRANSITIONS: {
                # proceed to the ("weather_flow", "extra") upon agreeing
                lbl.forward(): loc_cnd.condition_yes,
                ("weather_flow", "negative_node"): loc_cnd.condition_no
            }
        },
        "extra": {
            RESPONSE: rsp.extra_weather_response,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        },
        "negative_node": {
            RESPONSE: rsp.negative_weather,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        }
    },
    "light_flow": {
        "room": {
            RESPONSE: rsp.which_room,
            TRANSITIONS: {
                lbl.forward(): loc_cnd.room_condition,
                lbl.repeat(): cnd.true()
            }
        },
        "light_execution": {
            RESPONSE: rsp.light_response,
            TRANSITIONS: {
                ("dim_flow", "brightness", 1.1): cnd.all([loc_cnd.condition_yes, loc_cnd.dimmable_condition]),
                ("service_flow", "start_node", 1.1): cnd.any([loc_cnd.condition_no, loc_cnd.dimmable_condition]),
                lbl.to_start(): cnd.any([loc_cnd.condition_no, loc_cnd.condition_yes])
            }
        }
    },
    "dim_flow": {
        "room": {
            RESPONSE: rsp.which_dim,
            TRANSITIONS: {
                lbl.forward(): cnd.all([loc_cnd.dimmable_condition, loc_cnd.room_condition]),
                ("dim_flow", "not_available"): loc_cnd.room_condition,
                lbl.repeat(): cnd.true()
            }
        },
        "brightness": {
            RESPONSE: rsp.brightness,
            TRANSITIONS: {
                ("dim_flow", "dim_execution"): loc_cnd.get_brightness,
                lbl.repeat(): cnd.true()
            }
        },
        "dim_execution": {
            RESPONSE: rsp.dim_response,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        },
        "not_available": {
            RESPONSE: rsp.no_dim,
            TRANSITIONS: {
                lbl.to_start(): loc_cnd.condition_no,
                ("dim_flow", "room"): loc_cnd.condition_yes,
            }
        }
    },
    "climate_flow": {
        "room": {
            RESPONSE: rsp.which_room,
            TRANSITIONS: {
                lbl.forward(): loc_cnd.room_condition,
                lbl.repeat(): cnd.true()
            }
        },
        "set_temperature": {
            RESPONSE: rsp.temperature_setting,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        },
        "heat_up": {
            RESPONSE: rsp.heating_up,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        },
        "cool_down": {
            RESPONSE: rsp.cooling_down,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        }
    },
    "home_presence_flow": {
        "going_away": {
            RESPONSE: rsp.going_away,
            TRANSITIONS: {
                lbl.to_start(): loc_cnd.condition_yes,
                ("home_presence_flow", "asking"): loc_cnd.condition_no,
            }
        },
        "getting_in": {
            RESPONSE: rsp.getting_in,
            TRANSITIONS: {
                lbl.forward(): loc_cnd.condition_yes,
                lbl.to_start(): loc_cnd.condition_no
            }
        },
        "floor_heat": {
            RESPONSE: rsp.floor_heat,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        },
        "asking": {
            RESPONSE: rsp.should,
            TRANSITIONS: {
                lbl.forward(): loc_cnd.condition_yes,
                lbl.to_start(): loc_cnd.condition_no
            }
        },
        "lights_check": {
            RESPONSE: rsp.light_check,
            TRANSITIONS: {
                lbl.to_start(): cnd.true()
            }
        }
    }
}


actor = Actor(
    plot,
    start_label=("service_flow", "start_node"),
    fallback_label=("service_flow", "fallback_node")
)
