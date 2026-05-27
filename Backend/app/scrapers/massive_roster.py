import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine, Base
from app.models.player import Player

def calculate_ai_metrics(role, runs, matches, strike_rate, wickets, economy, is_marquee=False):
    impact = 0
    if "Batter" in role or role == "Wicketkeeper Batter":
        impact = ((runs / max(matches, 1)) * 0.5) + (strike_rate * 0.4)
    elif "Bowler" in role:
        impact = ((wickets / max(matches, 1)) * 25) + ((10 - economy) * 5)
    else: 
        impact = ((runs / max(matches, 1)) * 0.3) + (strike_rate * 0.25) + ((wickets / max(matches, 1)) * 15) + ((10 - economy) * 3)

    impact_score = round(min(max(impact, 40), 99.5), 1)

    # Corrected: Real IPL Base Price brackets with Marquee override
    if is_marquee: price = "₹2 Cr"
    elif impact_score > 90: price = "₹2 Cr"
    elif impact_score > 80: price = "₹1.5 Cr"
    elif impact_score > 70: price = "₹1 Cr"
    elif impact_score > 60: price = "₹50 Lakhs"
    else: price = "₹20 Lakhs"
    
    return impact_score, price

def generate_realistic_player(name, tier, assigned_team=None, assigned_role=None, is_marquee=False):
    """Generates realistic stats based on the player's tier"""
    if assigned_role:
        role = assigned_role
    else:
        roles = ["Top-order Batter", "Middle-order Batter", "Wicketkeeper Batter", "Batting Allrounder", "Bowling Allrounder", "Bowler", "Bowler"]
        role = random.choice(roles)
    
    # Base stats by tier
    if tier == "International":
        matches = random.randint(80, 200)
        team = assigned_team if assigned_team else random.choice(["IND", "AUS", "ENG", "SA", "NZ", "WI"])
    elif tier == "IPL Regular":
        matches = random.randint(40, 100)
        team = assigned_team if assigned_team else random.choice(["CSK", "MI", "RCB", "KKR", "SRH", "RR", "DC", "PBKS", "GT", "LSG"])
    else: # Ranji / Domestic
        matches = random.randint(10, 50)
        team = assigned_team if assigned_team else random.choice(["Mumbai", "Karnataka", "Tamil Nadu", "Delhi", "Saurashtra", "Vidarbha"])

    # Generate Stats based on role
    runs, wickets, strike_rate, average, economy = 0, 0, 0.0, 0.0, 0.0
    
    if "Batter" in role:
        runs = matches * random.randint(20, 35)
        average = round(random.uniform(25.0, 45.0), 2)
        strike_rate = round(random.uniform(120.0, 165.0), 2)
    elif "Bowler" in role:
        runs = matches * random.randint(2, 10)
        wickets = int(matches * random.uniform(0.8, 1.4))
        average = round(random.uniform(10.0, 25.0), 2)
        economy = round(random.uniform(6.5, 9.5), 2)
        strike_rate = round(random.uniform(90.0, 120.0), 2)
    else: # Allrounder
        runs = matches * random.randint(15, 25)
        wickets = int(matches * random.uniform(0.5, 1.0))
        average = round(random.uniform(20.0, 35.0), 2)
        strike_rate = round(random.uniform(130.0, 155.0), 2)
        economy = round(random.uniform(7.5, 9.0), 2)

    impact, price = calculate_ai_metrics(role, runs, matches, strike_rate, wickets, economy, is_marquee)
    
    return Player(
        name=name, role=role, team=team, batting_style="Right-hand bat" if random.random() > 0.3 else "Left-hand bat", 
        bowling_style="Right-arm fast" if random.random() > 0.5 else "Slow left-arm orthodox",
        matches=matches, runs=runs, highest_score=str(random.randint(60, 120)), batting_average=average, strike_rate=strike_rate,
        wickets=wickets, best_bowling=f"{random.randint(3,5)}/{random.randint(15,35)}", bowling_economy=economy, bowling_average=average,
        impact_score=impact, base_price_est=price
    )

def mass_seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Player).delete() # Clear old data
    db.commit()

    # REAL NAMES, 2026 TEAMS, and CORRECT ROLES
    international = [
        ("Pat Cummins", "SRH / AUS", "Bowling Allrounder"), ("Mitchell Starc", "DC / AUS", "Bowler"), ("Trent Boult", "MI / NZ", "Bowler"), 
        ("Heinrich Klaasen", "SRH / SA", "Wicketkeeper Batter"), ("Babar Azam", "PAK", "Top-order Batter"), ("Shaheen Afridi", "PAK", "Bowler"), 
        ("Travis Head", "SRH / AUS", "Top-order Batter"), ("Steve Smith", "AUS", "Middle-order Batter"), ("Kagiso Rabada", "GT / SA", "Bowler"), 
        ("Quinton de Kock", "KKR / SA", "Wicketkeeper Batter"), ("Glenn Maxwell", "PBKS / AUS", "Batting Allrounder"), ("Jos Buttler", "GT / ENG", "Wicketkeeper Batter"), 
        ("Sam Curran", "CSK / ENG", "Bowling Allrounder"), ("Nicholas Pooran", "LSG / WI", "Wicketkeeper Batter"), ("Andre Russell", "KKR / WI", "Batting Allrounder")
    ]
    
    ipl_stars = [
        ("Suryakumar Yadav", "MI / IND", "Middle-order Batter"), ("Ishan Kishan", "SRH / IND", "Wicketkeeper Batter"), ("Mohammed Siraj", "GT / IND", "Bowler"), 
        ("Mohammed Shami", "SRH / IND", "Bowler"), ("Yuzvendra Chahal", "PBKS / IND", "Bowler"), ("R. Ashwin", "CSK / IND", "Bowling Allrounder"), 
        ("KL Rahul", "DC / IND", "Wicketkeeper Batter"), ("Shreyas Iyer", "PBKS / IND", "Middle-order Batter"), ("Sanju Samson", "RR / IND", "Wicketkeeper Batter"), 
        ("Axar Patel", "DC / IND", "Bowling Allrounder"), ("Rishabh Pant", "LSG / IND", "Wicketkeeper Batter"), ("Arshdeep Singh", "PBKS / IND", "Bowler"), 
        ("Tilak Varma", "MI / IND", "Middle-order Batter"), ("Rinku Singh", "KKR / IND", "Middle-order Batter"), ("Yashasvi Jaiswal", "RR / IND", "Top-order Batter")
    ]
    
    ranji_grinders = [
        ("Sarfaraz Khan", "DC / Mumbai", "Middle-order Batter"), ("Abhimanyu Easwaran", "Bengal", "Top-order Batter"), ("Priyank Panchal", "Gujarat", "Top-order Batter"), 
        ("Jalaj Saxena", "Kerala", "Bowling Allrounder"), ("Shams Mulani", "MI / Mumbai", "Bowling Allrounder"), ("Rajat Patidar", "RCB / MP", "Top-order Batter"), 
        ("Sheldon Jackson", "Saurashtra", "Wicketkeeper Batter"), ("Baba Indrajith", "Tamil Nadu", "Wicketkeeper Batter"), ("Washington Sundar", "GT / TN", "Bowling Allrounder"), 
        ("Mayank Agarwal", "Karnataka", "Top-order Batter"), ("Venkatesh Iyer", "KKR / MP", "Batting Allrounder"), ("Jaydev Unadkat", "Saurashtra", "Bowler"), 
        ("Sandeep Sharma", "RR / Chandigarh", "Bowler"), ("Shahrukh Khan", "GT / TN", "Middle-order Batter"), ("Sai Kishore", "GT / TN", "Bowler"), 
        ("Harshit Rana", "KKR / Delhi", "Bowler"), ("Nitish Reddy", "SRH / Andhra", "Batting Allrounder"), ("Ashutosh Sharma", "DC / Railways", "Middle-order Batter"), 
        ("Shashank Singh", "PBKS / Chhattisgarh", "Batting Allrounder"), ("Naman Dhir", "MI / Punjab", "Batting Allrounder"), ("Nehal Wadhera", "PBKS / Punjab", "Middle-order Batter"), 
        ("Ramandeep Singh", "KKR / Punjab", "Batting Allrounder"), ("Suyash Sharma", "KKR / Delhi", "Bowler")
    ]
    
    # List of guaranteed marquee players to override their base price to ₹2 Cr
    marquee_list = [
        "Pat Cummins", "Mitchell Starc", "Trent Boult", "Heinrich Klaasen", 
        "Travis Head", "Steve Smith", "Kagiso Rabada", "Quinton de Kock", 
        "Glenn Maxwell", "Jos Buttler", "Sam Curran", "Andre Russell",
        "KL Rahul", "Shreyas Iyer", "Rishabh Pant", "Yuzvendra Chahal", 
        "Mohammed Shami", "Mohammed Siraj", "Suryakumar Yadav", "R. Ashwin"
    ]
    
    # Let's generate 150 more random names for the deep domestic circuit
    first_names = ["Rahul", "Amit", "Vikram", "Suresh", "Ravi", "Anil", "Deepak", "Akash", "Praveen", "Karan", "Vishal", "Mohit", "Aryan", "Prithvi", "Yash"]
    last_names = ["Sharma", "Singh", "Patel", "Kumar", "Yadav", "Gupta", "Desai", "Rao", "Joshi", "Chauhan", "Reddy", "Nair", "Iyer", "Verma", "Tiwari"]
    domestic_teams = ["Mumbai", "Karnataka", "Tamil Nadu", "Delhi", "Saurashtra", "Vidarbha", "Bengal", "Punjab", "Kerala", "MP"]
    domestic_unknowns = [(f"{random.choice(first_names)} {random.choice(last_names)}", random.choice(domestic_teams)) for _ in range(150)]

    all_players = []
    
    # Injecting precise names, teams, and ROLES now with marquee override
    for name, team, role in international: 
        all_players.append(generate_realistic_player(name, "International", team, role, is_marquee=(name in marquee_list)))
    for name, team, role in ipl_stars: 
        all_players.append(generate_realistic_player(name, "IPL Regular", team, role, is_marquee=(name in marquee_list)))
    for name, team, role in ranji_grinders: 
        all_players.append(generate_realistic_player(name, "Ranji", team, role, is_marquee=False))
    for name, team in domestic_unknowns: 
        all_players.append(generate_realistic_player(name, "Ranji", team, assigned_role=None, is_marquee=False))

    db.add_all(all_players)
    db.commit()
    print(f"✅ BOOM! Successfully injected {len(all_players)} players with CORRECT 2026 franchises and Marquee Base Prices into the database!")
    db.close()

if __name__ == "__main__":
    mass_seed_database()