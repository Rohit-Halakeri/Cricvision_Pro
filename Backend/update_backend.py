import os

def create_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ Created/Updated: {filepath}")

# --- 1. THE NEW PREDICTIONS API ---
PREDICTIONS_PY = """
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/predict", tags=["Predictions"])

class MatchSituation(BaseModel):
    target: int
    score: int
    overs: float
    wickets: int

class AuctionSituation(BaseModel):
    impact_score: float
    budget_cr: float

@router.post("/win")
def predict_win(sit: MatchSituation):
    runs_needed = sit.target - sit.score
    overs_left = 20.0 - sit.overs
    
    if runs_needed <= 0: return {"win_prob": 100.0, "status": "Team Batting Won"}
    if sit.wickets >= 10: return {"win_prob": 0.0, "status": "Team Bowling Won"}
    if overs_left <= 0: return {"win_prob": 0.0, "status": "Team Bowling Won"}

    crr = sit.score / max(sit.overs, 0.1)
    rrr = runs_needed / overs_left
    
    # Base 50% probability
    prob = 50.0
    prob += (crr - rrr) * 5.0  # Adjust by run rate pressure
    prob -= (sit.wickets * 4.0) # Penalty for lost wickets
    
    # Death over boost if wickets in hand
    if overs_left < 5 and sit.wickets < 5:
        prob += 15.0

    return {
        "win_prob": round(max(1.0, min(99.0, prob)), 1),
        "crr": round(crr, 2),
        "rrr": round(rrr, 2)
    }

@router.post("/auction")
def calculate_bid(sit: AuctionSituation):
    # Determine how much of the franchise budget they should spend
    # A 99 impact player is worth up to 25% of the total budget
    max_percentage = (sit.impact_score / 100) * 0.25 
    recommended_bid = sit.budget_cr * max_percentage
    
    strategy = "Value Pick"
    if sit.impact_score > 90: strategy = "Aggressive Marquee Bid"
    elif sit.impact_score > 75: strategy = "Strong Core Addition"
    
    return {
        "max_bid_cr": round(max_bid, 2),
        "strategy": strategy
    }
"""

# --- 2. UPDATE MAIN.PY TO INCLUDE THE NEW ROUTES ---
MAIN_PY = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import players, predictions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CricVision AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(predictions.router) # <-- NEW AI ROUTER ADDED

@app.get("/")
def read_root():
    return {"status": "online", "message": "CricVision Pro Backend is live!"}
"""

print("🚀 Upgrading Backend with AI prediction models...\n")
create_file("app/api/predictions.py", PREDICTIONS_PY)
create_file("app/main.py", MAIN_PY)
print("\n🎉 Backend upgrade complete! Please restart Uvicorn.")