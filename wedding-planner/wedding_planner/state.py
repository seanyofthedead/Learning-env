"""The shared "wedding file" that every node reads and updates."""
from typing import Annotated, ClassVar, Optional, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class Profile(BaseModel):
    """Facts about the wedding, pulled out of the conversation by the intake node."""

    names: Optional[str] = Field(None, description="The couple's names")
    date: Optional[str] = Field(None, description="Wedding date, e.g. 2027-06-12")
    city: Optional[str] = Field(None, description="City where the wedding happens")
    guests: Optional[int] = Field(None, description="Expected number of guests")
    budget: Optional[int] = Field(None, description="Total budget in US dollars")
    style: Optional[str] = Field(None, description="Style or vibe, e.g. rustic, modern")

    REQUIRED: ClassVar[tuple[str, ...]] = ("date", "city", "guests", "budget")

    def missing(self) -> list[str]:
        return [f for f in self.REQUIRED if getattr(self, f) in (None, "", 0)]


class WeddingState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    profile: dict  # Profile.model_dump() once intake is complete
    budget: dict  # category -> dollars allocated
    bookings: list[dict]  # vendors the couple approved
