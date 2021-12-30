from df_engine.core import Context
from .basic import binary_intent

def annotate(ctx: Context):
    # TODO: add your own annotators
    # add annotation in context
    ctx = binary_intent(ctx)
    return ctx
