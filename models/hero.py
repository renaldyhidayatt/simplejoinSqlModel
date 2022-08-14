from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
# from .team import Team

if TYPE_CHECKING:
    from .team import Team

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="heroes")

