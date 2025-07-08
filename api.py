from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
import os
from dotenv import load_dotenv
from agent import PersonalAIAgent
from pydantic import BaseModel

class AskInput(BaseModel):
    question: str

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
app = FastAPI()
agent = PersonalAIAgent()

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/ask")
async def ask(request: Request, data: AskInput):
    verify_token(request)
    try:
        response = agent.chat(data.question)
        return {"answer": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

