import sys
import os
import requests
import time
from bs4 import BeautifulSoup

# Allow script to find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine, Base
from app.models.player import Player

def scrape_cricbuzz_rankings():
    # We now loop through all three major ICC ranking categories!
    urls = [
        "https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting",
        "https://www.cricbuzz.com/cricket-stats/icc-rankings/men/bowling",
        "https://www.cricbuzz.com/cricket-stats/icc-rankings/men/all-rounder"
    ]
    
    # Websites block bots, so we trick them by pretending to be a real Google Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    db = SessionLocal()
    total_updated = 0

    print("🌍 Initiating full-spectrum stealth web scrape...\n")

    for url in urls:
        # Extract category name from URL for logging (BATTING, BOWLING, ALL-ROUNDER)
        category = url.split('/')[-1].upper()
        print(f"--- Scraping Top 20 {category} ---")
        
        try:
            # 1. DOWNLOAD THE WEBSITE
            response = requests.get(url, headers=headers)
            response.raise_for_status() 
            
            # 2. PARSE THE HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 3. EXTRACT THE DATA
            player_elements = soup.select('a.text-hvr-underline')

            scraped_names = []
            for element in player_elements[:20]: 
                name = element.text.strip()
                if name and "Profile" not in name: 
                    scraped_names.append(name)

            print(f"✅ Found {len(scraped_names)} top players in {category}!")
            
            # 4. UPDATE OUR SQLITE DATABASE
            category_updated = 0
            for name in scraped_names:
                search_name = name.split()[-1] if len(name.split()) > 1 else name
                db_player = db.query(Player).filter(Player.name.ilike(f"%{search_name}%")).first()
                
                if db_player:
                    print(f"🔥 BOOSTING: {db_player.name} (+3.0 Impact)")
                    db_player.impact_score = min(db_player.impact_score + 3.0, 99.5)
                    
                    if db_player.impact_score > 95:
                        db_player.base_price_est = "₹2 Cr (Marquee)"
                        
                    category_updated += 1
                    total_updated += 1

            print(f"Synced {category_updated} {category} players to database.\n")
            
            # Sleep for 2 seconds to avoid triggering anti-bot protection
            time.sleep(2)

        except Exception as e:
            print(f"❌ Scraping failed for {category}: {e}")

    db.commit()
    db.close()
    
    print(f"🚀 Full Database Sync Complete! {total_updated} players received live stat boosts.")

if __name__ == "__main__":
    scrape_cricbuzz_rankings()