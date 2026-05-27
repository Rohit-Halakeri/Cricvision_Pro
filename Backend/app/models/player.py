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
