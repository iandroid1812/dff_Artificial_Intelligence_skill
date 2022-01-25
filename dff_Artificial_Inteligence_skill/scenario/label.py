from typing import Optional, Callable
from df_engine.core import Actor, Context
from df_engine.core.types import NodeLabel3Type


def previous_fallback(priority: Optional[float] = None, *args, **kwargs) -> Callable:
    """
    Returns transition handler that takes :py:class:`~df_engine.core.context.Context`,
    :py:class:`~df_engine.core.actor.Actor` and :py:const:`priority <float>`.
    This handler returns a :py:const:`label <df_engine.core.types.NodeLabelType>`
    to the node before we went to the fallback node with a given :py:const:`priority <float>`.
    If the priority is not given, `Actor.label_priority` is used as default.

    Parameters
    -----------

    priority: Optional[float] = None
        float priority of transition. Uses `Actor.label_priority` if priority not defined.
    """

    def previous_fallback_handler(ctx: Context, actor: Actor, *args, **kwargs) -> NodeLabel3Type:
        current_priority = actor.label_priority if priority is None else priority
        if len(ctx.labels) >= 2:
            labels = list(ctx.labels.values())
            for item in labels[::-1]:
                if item != ('service_flow', 'fallback_node'):
                    return item[0], item[1], current_priority
        # if there is no labels other than fallback (for example error occurred in the beginning of convo)
        # we return the starting node
        return 'service_flow', 'start_node', current_priority

    return previous_fallback_handler
