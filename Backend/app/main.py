from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import players, predictions, chat, draft

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CricVision AI API", version="4.0.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(predictions.router) 
app.include_router(chat.router)
app.include_router(draft.router) # <-- PLAYING XI AUTO-DRAFT ADDED

@app.get("/")
def read_root():
    return {"status": "online", "message": "CricVision Pro AI Backend is live!"}
