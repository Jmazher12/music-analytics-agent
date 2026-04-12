import os
from dotenv import load_dotenv
load_dotenv()

from agents import set_tracing_disabled
set_tracing_disabled(True)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from my_agents.orchestrator import orchestrate

app = FastAPI(title="Music Analytics Agent")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class QueryRequest(BaseModel):
    query: str


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/api/ask")
async def ask(request: QueryRequest):
    try:
        result = await orchestrate(request.query)

        return JSONResponse({
            "success": True,
            "data_findings": result.get("data_findings", ""),
            "analysis": result.get("analysis", ""),
            "charts": result.get("charts", []),
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e),
        }, status_code=500)


@app.get("/health")
async def health():
    return {"status": "ok"}