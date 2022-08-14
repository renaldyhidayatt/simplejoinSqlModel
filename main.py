from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models.hero import Hero
from models.team import Team

# from sqlmodel.orm import join

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class TeamDto(BaseModel):
    name: str
    headquarters: str
    heroes: List[Hero]

class HeroDto(BaseModel):
    name: str
    secret_name: str
    age: int
    team_id: int






app = FastAPI()


@app.on_event("startup")
async def table_all():
    create_db_and_tables()


@app.get("/")
def Hello():
    return "Hello"


@app.get("/team", response_model=List[Team])
async def getAllTeam():
    db = Session(engine)
    query = db.query(Team).join(Hero).all()

    response = {
        "status": 'success',
        "data": query
    }    

    return query



@app.get("/heroes")
async def getAllHeroes():
    db = Session(engine)
    query= select(Hero, Team).join(Team)

    heroes = db.exec(query).all()

    return {"heroes": heroes}


@app.post("/team")
async def createTeam(team: TeamDto):
    db = Session(engine)
    db_team = Team(
        name=team.name,
        headquarters=team.headquarters
    )

    

    db.add(db_team)

    db.commit()

    response = {
        "status": "success"
    }

    return response


@app.post("/heroes")
async def createHeroes(hero: HeroDto):
    db = Session(engine)

    db_heroes = Hero(
        name=hero.name,
        secret_name=hero.secret_name,
        age=hero.age,
        team_id=hero.team_id
    )

    db.add(db_heroes)
    db.commit()

    response = {
        "status": "Success"
    }

    return response

    
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


