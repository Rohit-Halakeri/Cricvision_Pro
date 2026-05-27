import sys
import os

# Allow script to find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine, Base
from app.models.player import Player

def calculate_ai_metrics(role, runs, matches, strike_rate, wickets, economy):
    """Mini AI Algorithm to calculate Impact Score and Price"""
    impact = 0
    price = "Unsold"
    
    if "Batter" in role or role == "Wicketkeeper Batter":
        # Batting impact favors high strike rate and consistency
        impact = ((runs / max(matches, 1)) * 0.5) + (strike_rate * 0.4)
    elif "Bowler" in role:
        # Bowling impact favors lots of wickets and low economy
        impact = ((wickets / max(matches, 1)) * 25) + ((10 - economy) * 5)
    else: # Allrounder
        impact = ((runs / max(matches, 1)) * 0.3) + (strike_rate * 0.25) + ((wickets / max(matches, 1)) * 15) + ((10 - economy) * 3)

    # Normalize impact score to a 0-100 scale (cap at 99)
    impact_score = round(min(max(impact, 40), 99.5), 1)

    # Estimate price based on impact score
    if impact_score > 90: price = "₹15-20 Cr"
    elif impact_score > 80: price = "₹8-14 Cr"
    elif impact_score > 70: price = "₹4-7 Cr"
    elif impact_score > 60: price = "₹1-3 Cr"
    else: price = "Base Price (₹20L - 50L)"

    return impact_score, price

def mass_seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing players so we get a fresh, clean database
    db.query(Player).delete()
    db.commit()

    # Massive Roster of Real Players
    raw_players = [
        # --- INDIAN SUPERSTARS ---
        ("Rohit Sharma", "Opening Batter", "MI / IND", "Right-hand bat", "Right-arm offbreak", 257, 6628, 109, 29.72, 131.14, 15, "4/6", 8.02, 22.3),
        ("Shubman Gill", "Opening Batter", "GT / IND", "Right-hand bat", "Right-arm offbreak", 103, 3216, 129, 37.8, 135.2, 0, "-", 0.0, 0.0),
        ("Hardik Pandya", "Allrounder", "MI / IND", "Right-hand bat", "Right-arm medium-fast", 137, 2525, 91, 26.3, 145.8, 64, "3/17", 8.8, 33.5),
        ("Ravindra Jadeja", "Allrounder", "CSK / IND", "Left-hand bat", "Slow left-arm orthodox", 240, 2959, 62, 27.4, 128.7, 160, "5/16", 7.6, 29.2),
        ("Rishabh Pant", "Wicketkeeper Batter", "DC / IND", "Left-hand bat", None, 111, 3284, 128, 35.3, 148.9, 0, "-", 0.0, 0.0),
        
        # --- INTERNATIONAL HEAVYWEIGHTS ---
        ("Travis Head", "Opening Batter", "SRH / AUS", "Left-hand bat", "Right-arm offbreak", 38, 1121, 102, 33.9, 177.3, 2, "1/11", 9.5, 45.0),
        ("Rashid Khan", "Bowler", "GT / AFG", "Right-hand bat", "Legbreak googly", 121, 543, 79, 12.3, 145.2, 149, "4/24", 6.8, 21.8),
        ("Sunil Narine", "Allrounder", "KKR / WI", "Left-hand bat", "Right-arm offbreak", 177, 1534, 109, 17.2, 165.8, 180, "5/19", 6.7, 25.4),
        ("Trent Boult", "Bowler", "RR / NZ", "Right-hand bat", "Left-arm fast-medium", 104, 25, 6, 4.1, 89.2, 121, "4/18", 8.2, 26.5),
        ("Phil Salt", "Wicketkeeper Batter", "KKR / ENG", "Right-hand bat", None, 21, 653, 89, 34.3, 175.5, 0, "-", 0.0, 0.0),

        # --- DOMESTIC / EMERGING / RANJI STARS ---
        ("Riyan Parag", "Batting Allrounder", "RR / ASM", "Right-hand bat", "Legbreak", 69, 1173, 84, 23.4, 135.9, 7, "1/12", 9.8, 55.2),
        ("Mayank Yadav", "Bowler", "LSG / DEL", "Right-hand bat", "Right-arm fast", 4, 0, 0, 0.0, 0.0, 7, "3/14", 6.9, 12.1),
        ("Ruturaj Gaikwad", "Opening Batter", "CSK / MAH", "Right-hand bat", "Right-arm offbreak", 66, 2380, 108, 41.7, 136.8, 0, "-", 0.0, 0.0),
        ("Abhishek Sharma", "Batting Allrounder", "SRH / PUN", "Left-hand bat", "Slow left-arm orthodox", 63, 1377, 75, 25.5, 155.1, 9, "2/4", 8.9, 31.2),
        ("Sai Sudharsan", "Top-order Batter", "GT / TN", "Left-hand bat", "Legbreak", 25, 1034, 103, 47.0, 139.1, 0, "-", 0.0, 0.0),
        
        # --- VETERANS / CLASSICS ---
        ("MS Dhoni", "Wicketkeeper Batter", "CSK / IND", "Right-hand bat", "Right-arm medium", 264, 5243, 84, 39.1, 137.5, 0, "-", 0.0, 0.0),
        ("Glenn Maxwell", "Allrounder", "RCB / AUS", "Right-hand bat", "Right-arm offbreak", 134, 2771, 95, 24.7, 156.7, 37, "2/15", 8.3, 34.1),
        ("Jasprit Bumrah", "Bowler", "MI / IND", "Right-hand bat", "Right-arm fast", 133, 69, 16, 5.7, 85.1, 165, "5/10", 7.3, 22.5),
        ("Virat Kohli", "Top-order Batter", "RCB / IND", "Right-hand bat", "Right-arm medium", 252, 8004, 113, 38.6, 131.9, 4, "2/25", 8.8, 51.0),
        ("Heinrich Klaasen", "Wicketkeeper Batter", "SRH / SA", "Right-hand bat", "Right-arm offbreak", 55, 1245, 104, 35.8, 175.2, 0, "-", 0.0, 0.0)
    ]

    players_to_add = []
    for p in raw_players:
        # Calculate AI stats automatically based on their raw stats!
        impact, price = calculate_ai_metrics(p[1], p[6], p[5], p[9], p[10], p[12])
        
        players_to_add.append(
            Player(
                name=p[0], role=p[1], team=p[2], batting_style=p[3], bowling_style=p[4],
                matches=p[5], runs=p[6], highest_score=str(p[7]), batting_average=p[8], strike_rate=p[9],
                wickets=p[10], best_bowling=p[11], bowling_economy=p[12], bowling_average=p[13],
                impact_score=impact, base_price_est=price
            )
        )

    db.add_all(players_to_add)
    db.commit()
    print(f"✅ BOOM! Successfully injected {len(players_to_add)} players into the database with AI metrics!")
    db.close()

if __name__ == "__main__":
    print("Starting massive database expansion...")
    mass_seed_database()