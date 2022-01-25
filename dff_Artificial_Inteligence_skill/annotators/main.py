from df_engine.core import Context
import annotators.basic as basic


def annotate(ctx: Context):
    # add annotation in context
    ctx = basic.ctx_reset(ctx)
    ctx = basic.language_intent(ctx)
    ctx = basic.translate_request(ctx)
    ctx = basic.tts_status(ctx)
    ctx = basic.binary_intent(ctx)
    ctx = basic.room_intent(ctx)
    ctx = basic.numerical_values(ctx)
    ctx = basic.home_presence(ctx)
    return ctx
