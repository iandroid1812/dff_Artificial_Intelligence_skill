import df_engine.conditions as cnd
import df_engine.labels as lbl
from df_engine.core import Actor
from df_engine.core.keywords import RESPONSE, TRANSITIONS

import scenario.condition as loc_cnd
import scenario.response as rsp

# TODO: extend graph
plot = {
    "service_flow": {
        "start_node": {
            RESPONSE: rsp.awaiting,
            TRANSITIONS: {
                ("language_change", "node1"): loc_cnd.lang_condition,
                ("greeting_flow", "node1"): loc_cnd.greeting_condition,
                ("weather_flow", "basic"): loc_cnd.weather_condition,
                ("light_flow", "room"): loc_cnd.light_condition,
                ("dim_flow", "node1"): loc_cnd.dim_condition,
                ("climate_flow", "set_temperature"): loc_cnd.setting_temp_condition,
                ("climate_flow", "heat_up"): loc_cnd.heating_condition,
                ("climate_flow", "cool_down"): loc_cnd.cooling_condition
            }
        },
        "fallback_node": {
            RESPONSE: rsp.fallback, # issue
        }
    },
    "language_change": {
        "node1": {
            RESPONSE: rsp.language_change,
            TRANSITIONS: {
                ("service_flow", "start_node"): cnd.true()
            }
        }
    },
    "greeting_flow": {
        "node1": {
            RESPONSE: rsp.greet,
            TRANSITIONS: {
                ("weather_flow", "basic"): loc_cnd.weather_condition,
                ("light_flow", "room"): loc_cnd.light_condition,
                ("dim_flow", "node1"): loc_cnd.dim_condition,
                ("climate_flow", "set_temperature"): loc_cnd.setting_temp_condition,
                ("climate_flow", "heat_up"): loc_cnd.heating_condition,
                ("climate_flow", "cool_down"): loc_cnd.cooling_condition
            }
        }
    },
    "weather_flow": {
        "basic": {
            RESPONSE: rsp.basic_weather_response,
            TRANSITIONS: {
                ("weather_flow", "extra"): loc_cnd.condition_yes,
                ("weather_flow", "negative_node"): loc_cnd.condition_no
            }
        },
        "extra": {
            RESPONSE: rsp.extra_weather_response,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition
            }
        },
        "negative_node": {
            RESPONSE: rsp.negative_weather,
            TRANSITIONS: {
                ("service_flow", "start_node"): cnd.true()
            }
        }
    },
    "light_flow": {
        "room": {
            RESPONSE: rsp.which_room,
            TRANSITIONS: {
                ("light_flow", "node2"): loc_cnd.room_condition,
                lbl.repeat(): cnd.true()
            }
        },
        "node2": {
            RESPONSE: rsp.light_response,
            TRANSITIONS: {
                lbl.forward(): loc_cnd.check_dimmable, # issue
            }
        },
        "node3": {
            RESPONSE: rsp.want_dim,
            TRANSITIONS: {
                ("dim_flow", "node2"): loc_cnd.condition_yes
            }
        }
    },
    "dim_flow": {
        "node1": {
            RESPONSE: rsp.which_dim,
            TRANSITIONS: {
                ("dim_flow", "node2"): loc_cnd.check_dimmable,
                ("dim_flow", "not_available"): cnd.true()
            }
        },
        "node2": {
            RESPONSE: rsp.brightness,
            TRANSITIONS: {
                ("dim_flow", "dim_execution"): loc_cnd.get_brightness,
                lbl.repeat(): cnd.true()
            }
        },
        "dim_execution": {
            RESPONSE: rsp.dim_response,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition,
                ("service_flow", "start_node"): cnd.true()
            }
        },
        "not_available": {
            RESPONSE: rsp.no_dim,
            TRANSITIONS: {
                ("service_flow", "start_node"): cnd.true()
            }
        }
    },
    "climate_flow": {
        "set_temperature": {
            RESPONSE: rsp.temperature_setting,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition,
                ("service_flow", "start_node"): cnd.true()
            }
        },
        "heat_up": {
            RESPONSE: rsp.heating_up,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition,
                ("service_flow", "start_node"): cnd.true()
            }
        },
        "cool_down": {
            RESPONSE: rsp.cooling_down,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition,
                ("service_flow", "start_node"): cnd.true()
            }
        }
    },
    "appreciation_flow": {
        "node1": {
            RESPONSE: rsp.appreciate,
            TRANSITIONS: {
                ("service_flow", "start_node"): cnd.true()
            }
        }
    }
}


actor = Actor(
    plot,
    start_label=("service_flow", "start_node"),
    fallback_label=("service_flow", "fallback_node")
)


