"""Tools the vendor agent can call. The catalog is fake data; swap in a real API later."""
from langchain_core.tools import tool

VENDORS = [
    {"id": "V1", "category": "venue", "name": "Oak Hill Barn", "city": "Austin", "capacity": 150, "price": 9000, "style": "rustic"},
    {"id": "V2", "category": "venue", "name": "The Glass House", "city": "Austin", "capacity": 200, "price": 15000, "style": "modern"},
    {"id": "V3", "category": "venue", "name": "Lakeside Pavilion", "city": "Denver", "capacity": 120, "price": 8000, "style": "outdoor"},
    {"id": "C1", "category": "catering", "name": "Smoke & Sage BBQ", "city": "Austin", "capacity": 250, "price": 6500, "style": "rustic"},
    {"id": "C2", "category": "catering", "name": "Fig & Thyme", "city": "Austin", "capacity": 180, "price": 9500, "style": "modern"},
    {"id": "P1", "category": "photography", "name": "Golden Hour Studio", "city": "Austin", "capacity": 999, "price": 3200, "style": "any"},
    {"id": "P2", "category": "photography", "name": "Mile High Photo", "city": "Denver", "capacity": 999, "price": 2800, "style": "any"},
    {"id": "M1", "category": "music", "name": "DJ Two Step", "city": "Austin", "capacity": 999, "price": 1800, "style": "any"},
]


def get_vendor(vendor_id: str) -> dict | None:
    return next((v for v in VENDORS if v["id"] == vendor_id), None)


@tool
def search_vendors(category: str, city: str, guests: int, max_price: int) -> list[dict]:
    """Find vendors in a category (venue, catering, photography, music) that serve the city,
    fit the guest count and cost no more than max_price dollars."""
    return [
        v for v in VENDORS
        if v["category"] == category.lower()
        and v["city"].lower() == city.lower()
        and v["capacity"] >= guests
        and v["price"] <= max_price
    ]


@tool
def book_vendor(vendor_id: str) -> str:
    """Book a vendor by id. The couple is always asked to approve before it goes through."""
    # Never runs directly: the graph sends this call to the approval node instead.
    raise RuntimeError("book_vendor is handled by the approval node")


SEARCH_TOOLS = [search_vendors]
ALL_TOOLS = [search_vendors, book_vendor]
