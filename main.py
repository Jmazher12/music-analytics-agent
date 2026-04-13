import os
from dotenv import load_dotenv
load_dotenv()

import json

from agents import set_tracing_disabled
set_tracing_disabled(True)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from my_agents.orchestrator import orchestrate
from tools.search_tool import search_tracks as search_tracks_fn

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

@app.get("/api/search")
async def search(q: str):
    results = search_tracks_fn(q)
    return JSONResponse(json.loads(results))

@app.get("/api/track/{track_id}")
async def get_track(track_id: str):
    import sqlite3
    conn = sqlite3.connect("data/spotify_tracks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks WHERE track_id = ?", (track_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return JSONResponse(dict(row))
    return JSONResponse({"error": "Track not found"}, status_code=404)

@app.get("/health")
async def health():
    return {"status": "ok"}