from df_engine.core import Context
from .basic import language_intent, binary_intent, room_intent, numerical_values


def annotate(ctx: Context):
    # add annotation in context
    ctx = language_intent(ctx)
    ctx = binary_intent(ctx)
    ctx = room_intent(ctx)
    ctx = numerical_values(ctx)
    return ctx
