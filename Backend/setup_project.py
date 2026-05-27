import os

def create_file(filepath, content):
    if os.path.dirname(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ Created: {filepath}")

# --- FILE CONTENTS ---

REQ_TXT = """
fastapi
uvicorn
python-multipart
pandas
numpy
beautifulsoup4
requests
lxml
scikit-learn
xgboost
openai
langchain
SQLAlchemy
python-jose[cryptography]
passlib[bcrypt]
"""

DATABASE_PY = """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./cricvision.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

PLAYER_MODEL_PY = """
from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    team = Column(String)
    batting_style = Column(String)
    bowling_style = Column(String, nullable=True)
    
    matches = Column(Integer, default=0)
    runs = Column(Integer, default=0)
    highest_score = Column(String, nullable=True)
    batting_average = Column(Float, default=0.0)
    strike_rate = Column(Float, default=0.0)
    
    wickets = Column(Integer, default=0)
    best_bowling = Column(String, nullable=True)
    bowling_economy = Column(Float, default=0.0)
    bowling_average = Column(Float, default=0.0)
    
    impact_score = Column(Float, default=0.0)
    base_price_est = Column(String, nullable=True)
"""

PLAYERS_API_PY = """
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.player import Player

router = APIRouter(prefix="/api/players", tags=["Players"])

@router.get("/")
def get_all_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Player).offset(skip).limit(limit).all()

@router.get("/{player_id}")
def get_player_by_id(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return {"error": "Player not found"}
    return player
"""

MAIN_PY = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.models import player
from app.api import players

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CricVision AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Backend is running flawlessly!"}
"""

SEED_DB_PY = """
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine, Base
from app.models.player import Player

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Player).count() > 0:
        print("Database already seeded!")
        db.close()
        return

    players = [
        Player(name="Virat Kohli", role="Top-order Batter", team="RCB / IND", batting_style="Right-hand bat", matches=252, runs=8004, batting_average=38.66, strike_rate=131.97, impact_score=88.5, base_price_est="₹15-17 Cr"),
        Player(name="Jasprit Bumrah", role="Bowler", team="MI / IND", batting_style="Right-hand bat", bowling_style="Right-arm fast", matches=133, wickets=165, bowling_economy=7.30, bowling_average=22.51, impact_score=95.0, base_price_est="₹16-18 Cr")
    ]
    db.add_all(players)
    db.commit()
    print("Database seeded successfully with 2 players!")
    db.close()

if __name__ == "__main__":
    seed_database()
"""

# --- BUILD THE PROJECT ---
print("🚀 Building CricVision AI Project Structure...\n")

# Base requirements
create_file("requirements.txt", REQ_TXT)

# Adding __init__.py files fixes the "ModuleNotFoundError" automatically
create_file("app/__init__.py", "")
create_file("app/core/__init__.py", "")
create_file("app/models/__init__.py", "")
create_file("app/api/__init__.py", "")
create_file("app/scrapers/__init__.py", "")

# Write the actual code files
create_file("app/core/database.py", DATABASE_PY)
create_file("app/models/player.py", PLAYER_MODEL_PY)
create_file("app/api/players.py", PLAYERS_API_PY)
create_file("app/main.py", MAIN_PY)
create_file("app/scrapers/seed_db.py", SEED_DB_PY)

print("\n🎉 Project built successfully! All folders and files are in the right place.")
print("Now run these two commands in your terminal:")
print("  1. python -m app.scrapers.seed_db")
print("  2. uvicorn app.main:app --reload")