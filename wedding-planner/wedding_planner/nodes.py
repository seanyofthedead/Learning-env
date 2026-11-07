"""Graph nodes. Each takes the state and returns the parts of it to update."""
import json

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.types import interrupt

from . import budget as budget_lib
from .state import Profile, WeddingState
from .tools import ALL_TOOLS, get_vendor, search_vendors

INTAKE_PROMPT = (
    "Extract wedding details from the conversation. Leave a field empty if the couple "
    "has not said it. Do not guess."
)

VENDOR_PROMPT = """You are a friendly wedding planner helping with vendors.
Wedding: {profile}
Budget per category (USD): {budget}
Already booked: {bookings}
Money left overall: ${remaining}

Use search_vendors to find options, using the wedding's city and guest count and
the category budget as max_price unless the couple says otherwise. Compare a few
options briefly. Call book_vendor only when the couple clearly picks one."""

QUESTIONS = {
    "date": "the date (or rough month)",
    "city": "the city",
    "guests": "about how many guests",
    "budget": "your total budget",
}


def make_intake(llm):
    extractor = llm.with_structured_output(Profile)

    def intake(state: WeddingState):
        profile = extractor.invoke([SystemMessage(INTAKE_PROMPT), *state["messages"]])
        missing = profile.missing()
        if missing:
            ask = ", ".join(QUESTIONS[m] for m in missing)
            return {"messages": [AIMessage(f"Congratulations! To get started, tell me {ask}.")]}
        return {"profile": profile.model_dump()}

    return intake


def set_budget(state: WeddingState):
    """Deterministic step: split the total budget into categories."""
    plan = budget_lib.allocate(state["profile"]["budget"])
    lines = "\n".join(f"- {cat}: ${amt:,}" for cat, amt in plan.items())
    msg = (
        f"Here's a starting budget for {state['profile']['guests']} guests in "
        f"{state['profile']['city']}:\n{lines}\n\nWant me to look for a venue first?"
    )
    return {"budget": plan, "bookings": [], "messages": [AIMessage(msg)]}


def make_vendor_agent(llm):
    model = llm.bind_tools(ALL_TOOLS)

    def vendor_agent(state: WeddingState):
        bookings = state.get("bookings", [])
        system = VENDOR_PROMPT.format(
            profile=json.dumps(state["profile"]),
            budget=json.dumps(state["budget"]),
            bookings=json.dumps(bookings) if bookings else "nothing yet",
            remaining=f"{budget_lib.remaining(state['budget'], bookings):,}",
        )
        return {"messages": [model.invoke([SystemMessage(system), *state["messages"]])]}

    return vendor_agent


def approve_booking(state: WeddingState):
    """Human in the loop: pause the graph and ask the couple before booking."""
    last = state["messages"][-1]
    bookings = list(state.get("bookings", []))
    replies = []
    for call in last.tool_calls:
        if call["name"] != "book_vendor":
            # Run any other tool calls from the same message normally.
            result = search_vendors.invoke(call["args"])
            replies.append(ToolMessage(json.dumps(result), tool_call_id=call["id"]))
            continue

        vendor = get_vendor(call["args"].get("vendor_id", ""))
        if vendor is None:
            replies.append(ToolMessage("No vendor with that id.", tool_call_id=call["id"]))
            continue

        left = budget_lib.remaining(state["budget"], bookings)
        # interrupt() saves the state and stops here. The app shows this payload,
        # then resumes with Command(resume=True or False).
        approved = interrupt({
            "question": f"Book {vendor['name']} ({vendor['category']}) for ${vendor['price']:,}?",
            "vendor": vendor,
            "budget_left_after": left - vendor["price"],
        })
        if approved:
            bookings.append(vendor)
            text = f"Booked {vendor['name']}."
        else:
            text = f"The couple declined {vendor['name']}. Do not book it."
        replies.append(ToolMessage(text, tool_call_id=call["id"]))

    return {"messages": replies, "bookings": bookings}
