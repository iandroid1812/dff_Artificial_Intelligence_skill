from df_engine.core import Context
from .basic import binary_intent, lights_intent


def annotate(ctx: Context):
    # TODO: add your own annotators
    # add annotation in context
    ctx = binary_intent(ctx)
    ctx = lights_intent(ctx)
    return ctx
