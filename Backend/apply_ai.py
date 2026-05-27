import os

def create_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ Upgraded: {filepath}")

# --- 1. THE CHATBOT API (LANGCHAIN + SQL FALLBACK) ---
CHAT_PY = """
from fastapi import APIRouter
from pydantic import BaseModel
import os
import sqlite3

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

class ChatMessage(BaseModel):
    message: str

def smart_sql_fallback(msg: str):
    \"\"\"Acts as a fallback NLP agent if OpenAI API key is missing\"\"\"
    msg = msg.lower()
    conn = sqlite3.connect("cricvision.db")
    cursor = conn.cursor()
    
    try:
        if "highest strike rate" in msg:
            cursor.execute("SELECT name, strike_rate FROM players ORDER BY strike_rate DESC LIMIT 1")
            row = cursor.fetchone()
            return f"The player with the highest strike rate is {row[0]} with a massive {row[1]} SR!"
        elif "most wickets" in msg:
            cursor.execute("SELECT name, wickets FROM players ORDER BY wickets DESC LIMIT 1")
            row = cursor.fetchone()
            return f"{row[0]} has the most wickets in the database with {row[1]} scalps."
        elif "most runs" in msg or "highest runs" in msg:
            cursor.execute("SELECT name, runs FROM players ORDER BY runs DESC LIMIT 1")
            row = cursor.fetchone()
            return f"The top run-scorer is {row[0]} with {row[1]} runs!"
        elif "marquee" in msg or "2 cr" in msg:
            cursor.execute("SELECT count(*) FROM players WHERE base_price_est = '₹2 Cr'")
            row = cursor.fetchone()
            return f"There are {row[0]} marquee players in the database commanding a ₹2 Cr base price."
        else:
            return "I am the CricVision AI! Try asking me 'Who has the most wickets?' or 'Who has the highest strike rate?' (Add an OPENAI_API_KEY to your environment to unlock full LangChain capabilities!)"
    except Exception as e:
        return "Sorry, I had trouble querying the database."
    finally:
        conn.close()

@router.post("/")
def chat_with_data(req: ChatMessage):
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Use real LangChain if API key exists
    if api_key and api_key != "your-key-here":
        try:
            from langchain_community.utilities import SQLDatabase
            from langchain_community.agent_toolkits import create_sql_agent
            from langchain_openai import ChatOpenAI
            
            db = SQLDatabase.from_uri("sqlite:///./cricvision.db")
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
            agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
            
            response = agent_executor.invoke({"input": req.message})
            return {"reply": response["output"]}
        except Exception as e:
            return {"reply": f"LangChain Error: {str(e)}"}
            
    # Fallback to Smart SQL if no key
    return {"reply": smart_sql_fallback(req.message)}
"""

# --- 2. UPDATED PREDICTIONS API (NOW USING TRUE ML) ---
PREDICTIONS_PY = """
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
    \"\"\"Uses the trained RandomForest model to predict impact\"\"\"
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
"""

# --- 3. UPDATE MAIN.PY TO REGISTER CHATBOT ---
MAIN_PY = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import players, predictions, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CricVision AI API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(predictions.router) 
app.include_router(chat.router) # <-- CHATBOT ADDED

@app.get("/")
def read_root():
    return {"status": "online", "message": "CricVision Pro AI Backend is live!"}
"""

print("🚀 Injecting Machine Learning and LangChain Chatbot routes...\n")
create_file("app/api/chat.py", CHAT_PY)
create_file("app/api/predictions.py", PREDICTIONS_PY)
create_file("app/main.py", MAIN_PY)
print("\n🎉 AI Upgrade complete! Restart Uvicorn to apply changes.")