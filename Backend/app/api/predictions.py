from fastapi import APIRouter
from pydantic import BaseModel
import pickle
import os
import pandas as pd

router = APIRouter(prefix="/api/predict", tags=["Predictions"])

# Load the trained ML Model!
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "impact_model.pkl")
ml_model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)

class MatchSituation(BaseModel):
    target: int
    score: int
    overs: float
    wickets: int

class AuctionSituation(BaseModel):
    impact_score: float
    budget_cr: float

class PlayerStats(BaseModel):
    matches: int
    runs: int
    batting_average: float
    strike_rate: float
    wickets: int
    bowling_economy: float

@router.post("/true_impact")
def predict_true_impact(stats: PlayerStats):
    """Uses the trained RandomForest model to predict impact"""
    if ml_model is None:
        return {"error": "ML Model not trained! Run train_model.py first.", "impact": 0}
    
    # Create DataFrame matching exactly what the model was trained on
    input_data = pd.DataFrame([{
        "matches": stats.matches,
        "runs": stats.runs,
        "batting_average": stats.batting_average,
        "strike_rate": stats.strike_rate,
        "wickets": stats.wickets,
        "bowling_economy": stats.bowling_economy
    }])
    
    prediction = ml_model.predict(input_data)[0]
    return {"predicted_impact": round(prediction, 1)}

@router.post("/win")
def predict_win(sit: MatchSituation):
    runs_needed = sit.target - sit.score
    overs_left = 20.0 - sit.overs
    if runs_needed <= 0: return {"win_prob": 100.0, "status": "Team Batting Won"}
    if sit.wickets >= 10 or overs_left <= 0: return {"win_prob": 0.0, "status": "Team Bowling Won"}
    crr = sit.score / max(sit.overs, 0.1)
    rrr = runs_needed / max(overs_left, 0.1)
    prob = 50.0 + ((crr - rrr) * 5.0) - (sit.wickets * 4.0)
    if overs_left < 5 and sit.wickets < 5: prob += 15.0
    return {"win_prob": round(max(1.0, min(99.0, prob)), 1), "crr": round(crr, 2), "rrr": round(rrr, 2)}

@router.post("/auction")
def calculate_bid(sit: AuctionSituation):
    max_percentage = (sit.impact_score / 100) * 0.25 
    max_bid = sit.budget_cr * max_percentage 
    strategy = "Value Pick"
    if sit.impact_score > 90: strategy = "Aggressive Marquee Bid"
    elif sit.impact_score > 75: strategy = "Strong Core Addition"
    return {"max_bid_cr": round(max_bid, 2), "strategy": strategy}
