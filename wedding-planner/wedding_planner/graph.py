"""Wire the nodes into a LangGraph StateGraph.

    START -> (no profile yet?) -> intake -> (complete?) -> set_budget -> END
          -> (profile known)   -> vendor_agent -> tools ----------> vendor_agent
                                               -> approve_booking -> vendor_agent
                                               -> END
"""
import os

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from .nodes import approve_booking, make_intake, make_vendor_agent, set_budget
from .state import WeddingState
from .tools import SEARCH_TOOLS

DEFAULT_MODEL = "anthropic:claude-sonnet-5-5"


def route_start(state: WeddingState):
    return "vendor_agent" if state.get("profile") else "intake"


def route_after_intake(state: WeddingState):
    return "set_budget" if state.get("profile") else END


def route_after_agent(state: WeddingState):
    calls = getattr(state["messages"][-1], "tool_calls", None)
    if not calls:
        return END
    if any(c["name"] == "book_vendor" for c in calls):
        return "approve_booking"
    return "tools"


def build_graph(llm=None, checkpointer=None):
    if llm is None:
        from langchain.chat_models import init_chat_model

        llm = init_chat_model(os.getenv("WEDDING_MODEL", DEFAULT_MODEL))

    g = StateGraph(WeddingState)
    g.add_node("intake", make_intake(llm))
    g.add_node("set_budget", set_budget)
    g.add_node("vendor_agent", make_vendor_agent(llm))
    g.add_node("tools", ToolNode(SEARCH_TOOLS))
    g.add_node("approve_booking", approve_booking)

    g.add_conditional_edges(START, route_start, ["intake", "vendor_agent"])
    g.add_conditional_edges("intake", route_after_intake, ["set_budget", END])
    g.add_edge("set_budget", END)
    g.add_conditional_edges("vendor_agent", route_after_agent, ["tools", "approve_booking", END])
    g.add_edge("tools", "vendor_agent")
    g.add_edge("approve_booking", "vendor_agent")

    # The checkpointer saves state per thread_id, so a couple can come back later.
    # Swap InMemorySaver for a SQLite or Postgres saver to keep it across restarts.
    return g.compile(checkpointer=checkpointer or InMemorySaver())
