from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agent import PersonalAIAgent

# === Chargement des variables d'environnement
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# === Initialisation de FastAPI + Sécurité Bearer
auth_scheme = HTTPBearer()
app = FastAPI(
    title="Agent IA Personnel",
    description="API FastAPI sécurisée pour interagir avec un assistant IA",
    version="1.0.0"
)

# === Chargement de l'agent IA
agent = PersonalAIAgent()

# === Schéma d'entrée pour /ask
class AskInput(BaseModel):
    question: str

# === Endpoint sécurisé
@app.post("/ask")
async def ask(
    data: AskInput,
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    if credentials.scheme != "Bearer" or credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = agent.chat(data.question)
        return {"answer": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
