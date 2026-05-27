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
