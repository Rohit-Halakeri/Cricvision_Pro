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
