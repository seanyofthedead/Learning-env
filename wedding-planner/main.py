"""Chat with the planner in the terminal: python main.py"""
import uuid

from langgraph.types import Command

from wedding_planner import build_graph


def main():
    app = build_graph()
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    print("Wedding planner. Type 'quit' to stop.\n")

    while True:
        text = input("you> ").strip()
        if text.lower() in {"quit", "exit"}:
            break
        result = app.invoke({"messages": [("user", text)]}, config)

        # The graph pauses at approve_booking until we answer.
        while result.get("__interrupt__"):
            ask = result["__interrupt__"][0].value
            print(f"\n{ask['question']}  (budget left after: ${ask['budget_left_after']:,})")
            yes = input("approve? [y/n]> ").strip().lower().startswith("y")
            result = app.invoke(Command(resume=yes), config)

        print(f"\nplanner> {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()
