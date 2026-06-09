from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

from pipeline import run_pipeline

app = FastAPI(title="Research Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html at root
@app.get("/")
def root():
    return FileResponse("index.html")


class ResearchRequest(BaseModel):
    topic: str
    gemini_key: str = ""
    tavily_key: str = ""


@app.post("/research")
def research(body: ResearchRequest):
    # Use keys from request if provided, else fall back to .env
    if body.gemini_key:
        os.environ["GOOGLE_API_KEY"] = body.gemini_key
    if body.tavily_key:
        os.environ["TAVILY_API_KEY"] = body.tavily_key

    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=400, detail="Missing GOOGLE_API_KEY — add it in the UI or set it in .env")
    if not os.getenv("TAVILY_API_KEY"):
        raise HTTPException(status_code=400, detail="Missing TAVILY_API_KEY — add it in the UI or set it in .env")

    try:
        state = run_pipeline(body.topic)
        return {
            "report":   state.get("report", ""),
            "feedback": state.get("feedback", ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
