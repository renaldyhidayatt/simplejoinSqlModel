from typing import Optional,List
from sqlmodel import SQLModel, Field, Relationship
from .hero import Hero

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    heroes: Optional["Hero"] = Relationship(back_populates="team")