from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.player import Player
import re

router = APIRouter(prefix="/api/predict", tags=["Draft"])

class DraftRequest(BaseModel):
    budget_cr: float

@router.post("/auto-draft")
def auto_draft_squad(request: DraftRequest, db: Session = Depends(get_db)):
    players = db.query(Player).all()
    
    requirements = { "Batter": 4, "Wicketkeeper": 1, "Allrounder": 2, "Bowler": 4 }
    squad = []
    total_spent = 0.0
    total_impact = 0.0
    
    def extract_price(price_str):
        if not price_str: return 0.2
        if "Cr" in price_str:
            match = re.search(r'\d+(\.\d+)?', price_str)
            return float(match.group()) if match else 2.0
        elif "L" in price_str or "Lakhs" in price_str:
            match = re.search(r'\d+', price_str)
            return float(match.group()) / 100 if match else 0.2
        return 0.2

    for p in players:
        p.price_val = extract_price(p.base_price_est)
        p.value_for_money = p.impact_score / p.price_val if p.price_val > 0 else 0

    sorted_players = sorted(players, key=lambda x: x.value_for_money, reverse=True)
    
    for p in sorted_players:
        if len(squad) == 11: break
            
        role_key = "Batter"
        if "Wicketkeeper" in p.role: role_key = "Wicketkeeper"
        elif "Allrounder" in p.role: role_key = "Allrounder"
        elif "Bowler" in p.role: role_key = "Bowler"
        
        if requirements[role_key] > 0 and (total_spent + p.price_val) <= request.budget_cr:
            squad.append({
                "name": p.name, "role": p.role, "team": p.team,
                "impact_score": p.impact_score, "price": f"₹{p.price_val} Cr"
            })
            total_spent += p.price_val
            total_impact += p.impact_score
            requirements[role_key] -= 1

    return {
        "squad": squad,
        "total_spent_cr": round(total_spent, 2),
        "total_impact": round(total_impact, 2),
        "players_drafted": len(squad)
    }
