"""Plain-Python budget logic. Not everything needs an LLM."""

# Typical US split of a wedding budget.
SPLIT = {
    "venue": 0.40,
    "catering": 0.25,
    "photography": 0.12,
    "music": 0.08,
    "flowers": 0.08,
    "other": 0.07,
}


def allocate(total: int) -> dict[str, int]:
    return {cat: round(total * share) for cat, share in SPLIT.items()}


def spent(bookings: list[dict]) -> int:
    return sum(b["price"] for b in bookings)


def remaining(budget: dict[str, int], bookings: list[dict]) -> int:
    return sum(budget.values()) - spent(bookings)
