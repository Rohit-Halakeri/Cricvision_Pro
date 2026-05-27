from fastapi import APIRouter
from pydantic import BaseModel
import os
import sqlite3

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

class ChatMessage(BaseModel):
    message: str

def smart_sql_fallback(msg: str):
    """Acts as a fallback NLP agent if OpenAI API key is missing"""
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
