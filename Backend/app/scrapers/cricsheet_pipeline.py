import sys
import os
import requests
import zipfile
import io
import pandas as pd
from sqlalchemy.orm import Session

# Allow script to find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine, Base
from app.models.player import Player

def calculate_ai_metrics(role, runs, matches, strike_rate, wickets, economy, is_marquee=False):
    """Reusing our trusted AI Impact Calculator"""
    impact = 0
    if "Batter" in role or role == "Wicketkeeper Batter":
        impact = ((runs / max(matches, 1)) * 0.5) + (strike_rate * 0.4)
    elif "Bowler" in role:
        impact = ((wickets / max(matches, 1)) * 25) + ((10 - economy) * 5)
    else: 
        impact = ((runs / max(matches, 1)) * 0.3) + (strike_rate * 0.25) + ((wickets / max(matches, 1)) * 15) + ((10 - economy) * 3)

    impact_score = round(min(max(impact, 40), 99.5), 1)

    if is_marquee: price = "₹2 Cr (Marquee)"
    elif impact_score > 90: price = "₹2 Cr"
    elif impact_score > 80: price = "₹1.5 Cr"
    elif impact_score > 70: price = "₹1 Cr"
    elif impact_score > 60: price = "₹50 Lakhs"
    else: price = "₹20 Lakhs"
    
    return impact_score, price

def run_cricsheet_pipeline():
    print("🚀 [STAGE 1: EXTRACT] Downloading Cricsheet IPL ball-by-ball dataset...")
    
    # Official Cricsheet URL for IPL CSVs
    zip_url = "https://cricsheet.org/downloads/ipl_csv2.zip"
    
    response = requests.get(zip_url)
    response.raise_for_status()
    print("✅ Download complete! Extracting data in memory...")

    # Open the zip file in RAM
    z = zipfile.ZipFile(io.BytesIO(response.content))
    
    # Filter out only the match CSV files (ignoring info files and READMEs)
    csv_files = [f for f in z.namelist() if f.endswith('.csv') and not f.endswith('_info.csv')]
    
    # To prevent this taking 10 minutes on a laptop, we'll process the latest 150 matches. 
    # (In production, you'd process all 1000+ files)
    csv_files = csv_files[-150:] 
    
    print(f"📊 [STAGE 2: TRANSFORM] Crunching ball-by-ball data for {len(csv_files)} matches using Pandas...")
    
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(z.open(file))
        dataframes.append(df)
        
    # Combine all matches into one massive DataFrame
    full_df = pd.concat(dataframes, ignore_index=True)
    
    print(f"🧠 Processing {len(full_df)} individual deliveries...")

    # --- BATTING STATS AGGREGATION ---
    batting = full_df.groupby('striker').agg(
        runs=('runs_off_bat', 'sum'),
        balls_faced=('ball', 'count'),
        matches=('match_id', 'nunique')
    ).reset_index()
    batting['strike_rate'] = round((batting['runs'] / batting['balls_faced']) * 100, 2)
    
    # --- BOWLING STATS AGGREGATION ---
    # Filter for real wickets (excluding run outs, retired hurt, etc)
    wickets_df = full_df[full_df['wicket_type'].notna() & ~full_df['wicket_type'].isin(['run out', 'retired hurt', 'obstructing the field'])]
    bowler_wickets = wickets_df.groupby('bowler').size().reset_index(name='wickets')
    
    bowling_runs = full_df.groupby('bowler').agg(
        runs_conceded=('runs_off_bat', 'sum'), # Oversimplified for speed
        balls_bowled=('ball', 'count'),
        matches=('match_id', 'nunique')
    ).reset_index()
    
    bowling = pd.merge(bowling_runs, bowler_wickets, on='bowler', how='left').fillna(0)
    bowling['overs'] = bowling['balls_bowled'] / 6
    bowling['economy'] = round(bowling['runs_conceded'] / bowling['overs'], 2)

    print("💾 [STAGE 3: LOAD] Updating SQLite Database with real historical data...")
    
    db = SessionLocal()
    
    # Let's update batters in our database
    updated_count = 0
    for _, row in batting.iterrows():
        player_name = row['striker']
        # Search for player by last name for better matching
        search_name = player_name.split()[-1] if len(player_name.split()) > 1 else player_name
        
        db_player = db.query(Player).filter(Player.name.ilike(f"%{search_name}%")).first()
        
        if db_player:
            # Update real stats
            db_player.runs = int(row['runs'])
            db_player.strike_rate = float(row['strike_rate'])
            # Only update matches if the Cricsheet count is higher than what we generated
            db_player.matches = max(db_player.matches, int(row['matches']))
            
            # Recalculate AI Score based on these REAL numbers
            impact, price = calculate_ai_metrics(
                db_player.role, db_player.runs, db_player.matches, 
                db_player.strike_rate, db_player.wickets, db_player.bowling_economy, 
                is_marquee=("Cr" in str(db_player.base_price_est))
            )
            db_player.impact_score = impact
            db_player.base_price_est = price
            updated_count += 1

    # Update bowlers
    for _, row in bowling.iterrows():
        player_name = row['bowler']
        search_name = player_name.split()[-1] if len(player_name.split()) > 1 else player_name
        
        db_player = db.query(Player).filter(Player.name.ilike(f"%{search_name}%")).first()
        
        if db_player:
            db_player.wickets = int(row['wickets'])
            db_player.bowling_economy = float(row['economy'])
            
            impact, price = calculate_ai_metrics(
                db_player.role, db_player.runs, db_player.matches, 
                db_player.strike_rate, db_player.wickets, db_player.bowling_economy, 
                is_marquee=("Cr" in str(db_player.base_price_est))
            )
            db_player.impact_score = impact
            db_player.base_price_est = price
            updated_count += 1

    db.commit()
    db.close()
    
    print(f"🎉 ETL Pipeline Complete! Synthesized {updated_count} player profiles using Cricsheet industrial data.")

if __name__ == "__main__":
    run_cricsheet_pipeline()