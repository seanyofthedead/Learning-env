"""Run the whole graph with a scripted fake model, so no API key is needed."""
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import Command

from wedding_planner import build_graph
from wedding_planner.budget import allocate
from wedding_planner.state import Profile
from wedding_planner.tools import search_vendors


class Scripted:
    def __init__(self, replies):
        self.replies = list(replies)
        self.seen = []

    def invoke(self, messages):
        self.seen.append(messages)
        return self.replies.pop(0)


class FakeLLM:
    """Stands in for a chat model: queued answers for intake and for the vendor agent."""

    def __init__(self, profiles=(), agent_replies=()):
        self.extract = Scripted(profiles)
        self.agent = Scripted(agent_replies)

    def with_structured_output(self, schema):
        return self.extract

    def bind_tools(self, tools):
        return self.agent


def call(name, args, id):
    return AIMessage("", tool_calls=[{"name": name, "args": args, "id": id}])


FULL = Profile(names="Ana & Ben", date="2027-06-12", city="Austin", guests=120, budget=40000)
CFG = {"configurable": {"thread_id": "t1"}}


def test_budget_split_adds_up():
    assert sum(allocate(40000).values()) == 40000


def test_search_filters_by_city_size_and_price():
    found = search_vendors.invoke({"category": "venue", "city": "Austin", "guests": 120, "max_price": 16000})
    assert [v["id"] for v in found] == ["V1", "V2"]
    found = search_vendors.invoke({"category": "venue", "city": "Austin", "guests": 120, "max_price": 10000})
    assert [v["id"] for v in found] == ["V1"]


def test_intake_asks_for_missing_details():
    app = build_graph(FakeLLM(profiles=[Profile(city="Austin")]))
    out = app.invoke({"messages": [("user", "We're getting married in Austin!")]}, CFG)
    assert "profile" not in out
    reply = out["messages"][-1].content
    assert "date" in reply and "guests" in reply and "budget" in reply


def test_full_flow_search_then_approved_booking():
    llm = FakeLLM(
        profiles=[FULL],
        agent_replies=[
            call("search_vendors", {"category": "venue", "city": "Austin", "guests": 120, "max_price": 16000}, "s1"),
            AIMessage("Oak Hill Barn ($9,000) or The Glass House ($15,000)?"),
            call("book_vendor", {"vendor_id": "V1"}, "b1"),
            AIMessage("Done! Oak Hill Barn is booked."),
        ],
    )
    app = build_graph(llm)

    # Turn 1: intake completes, budget is set.
    out = app.invoke({"messages": [("user", "Ana & Ben, Austin, June 12 2027, 120 guests, $40k")]}, CFG)
    assert out["budget"]["venue"] == 16000

    # Turn 2: the agent searches (tool runs) and then answers.
    out = app.invoke({"messages": [("user", "Find us a venue")]}, CFG)
    assert any(isinstance(m, ToolMessage) and "Oak Hill Barn" in m.content for m in out["messages"])
    assert "Glass House" in out["messages"][-1].content

    # Turn 3: the agent tries to book, so the graph pauses for approval.
    out = app.invoke({"messages": [("user", "Book the barn")]}, CFG)
    ask = out["__interrupt__"][0].value
    assert "Oak Hill Barn" in ask["question"]
    assert ask["budget_left_after"] == 31000
    assert app.get_state(CFG).values["bookings"] == []

    out = app.invoke(Command(resume=True), CFG)
    assert [b["id"] for b in out["bookings"]] == ["V1"]
    assert out["messages"][-1].content == "Done! Oak Hill Barn is booked."


def test_declined_booking_is_not_saved():
    llm = FakeLLM(
        profiles=[FULL],
        agent_replies=[call("book_vendor", {"vendor_id": "V2"}, "b1"), AIMessage("No problem.")],
    )
    app = build_graph(llm)
    app.invoke({"messages": [("user", "details...")]}, CFG)
    app.invoke({"messages": [("user", "Book the Glass House")]}, CFG)
    out = app.invoke(Command(resume=False), CFG)
    assert out["bookings"] == []
    assert any(isinstance(m, ToolMessage) and "declined" in m.content for m in out["messages"])
