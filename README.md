# Music Analytics Agent
 
A multi-agent system that performs data collection, exploratory data analysis, and hypothesis formation on a dataset of 89,000+ Spotify tracks across 125 genres.
 
**Deployed URL:** _[Add Cloud Run URL after deployment]_
 
---
 
## How It Works
 
Ask a question about music data, and three AI agents collaborate to answer it:
 
1. **Data Agent** — Collects relevant data by writing and executing SQL queries against the Spotify database, and retrieves background knowledge from a vector store
2. **Analyst Agent** — Analyzes the findings, forms a data-driven hypothesis, and generates visualizations
3. **Orchestrator** — Coordinates the pipeline: routes the user's question to the Data Agent, passes findings to the Analyst Agent, and returns the combined results
 
## The Three Steps
 
### Step 1: Collect
The Data Agent retrieves data at runtime using two methods:
- **SQL composition** — Dynamically writes and executes SQL queries against a SQLite database of 89,740 Spotify tracks (`tools/sql_tool.py` → `run_sql_query()`)
- **RAG retrieval** — Searches a ChromaDB vector store containing music domain knowledge about audio features, genres, and analysis frameworks (`tools/rag_tool.py` → `search_music_knowledge()`)
 
The SQL queries adapt to the user's question. Asking "What is the most popular genre?" produces different queries than "Compare danceability of rock vs jazz."
 
### Step 2: Explore and Analyze (EDA)
The Data Agent performs exploratory analysis by running multiple SQL queries with aggregation functions (AVG, COUNT, GROUP BY, ORDER BY) to compute statistics, compare groups, and surface patterns. This is done through the `query_spotify_db` tool in `my_agents/data_agent.py`.
 
The exploration is dynamic — different questions trigger different SQL queries and different aggregations. The agent examines the data before reasoning about it, surfacing specific numbers and patterns that feed into the hypothesis phase.
 
### Step 3: Hypothesize
The Analyst Agent (`my_agents/analyst_agent.py`) receives the Data Agent's findings and:
- Forms a clear hypothesis statement grounded in specific data points
- Cites supporting evidence with actual numbers from the queries
- Generates a visualization (bar chart, scatter plot, or line chart) to complement the hypothesis
- Discusses caveats and alternative explanations
 
---
 
## Core Requirements
 
| Requirement | Implementation | Location |
|-------------|---------------|----------|
| **Frontend** | HTML/CSS/JS single-page app with query input, markdown rendering, and chart display | `static/index.html` |
| **Agent framework** | OpenAI Agents SDK with LiteLLM integration for Vertex AI | `my_agents/data_agent.py`, `my_agents/analyst_agent.py` |
| **Tool calling** | SQL tool, RAG tool, and three chart tools | `tools/sql_tool.py`, `tools/rag_tool.py`, `tools/chart_tool.py` |
| **Non-trivial dataset** | 89,740 Spotify tracks with 20 columns across 125 genres (Kaggle dataset loaded into SQLite) | `data/spotify_tracks.db` (built by `data/setup_db.py`) |
| **Multi-agent pattern** | Orchestrator-handoff: Orchestrator → Data Agent → Analyst Agent, each with distinct system prompts and responsibilities | `my_agents/orchestrator.py` |
| **Deployed** | Google Cloud Run with Vertex AI authentication | _[URL above]_ |
| **README.md** | This file | `README.md` |
 
## Grab Bag
 
| Technique | Implementation | Location |
|-----------|---------------|----------|
| **Second data retrieval method** | SQL composition + RAG retrieval. The Data Agent uses both SQL queries against the Spotify database and vector search against the ChromaDB knowledge base | `tools/sql_tool.py` → `run_sql_query()`, `tools/rag_tool.py` → `search_music_knowledge()` |
| **Data Visualization** | The Analyst Agent generates matplotlib charts (bar, scatter, line) encoded as base64 PNG images and displayed in the frontend | `tools/chart_tool.py` → `create_bar_chart()`, `create_scatter_plot()`, `create_line_chart()` |
 
---
 
## Project Structure
 
```
music-analytics-agent/
├── my_agents/
│   ├── __init__.py
│   ├── data_agent.py          # Data collection & EDA agent
│   ├── analyst_agent.py       # Hypothesis & visualization agent
│   └── orchestrator.py        # Coordinates the multi-agent pipeline
├── tools/
│   ├── __init__.py
│   ├── sql_tool.py            # SQL query execution against Spotify DB
│   ├── rag_tool.py            # ChromaDB vector search
│   └── chart_tool.py          # Matplotlib chart generation
├── data/
│   ├── knowledge/
│   │   ├── spotify_audio_features.md
│   │   ├── music_genres.md
│   │   └── music_analysis_frameworks.md
│   ├── setup_db.py            # Loads CSV into SQLite
│   ├── setup_rag.py           # Loads knowledge files into ChromaDB
│   └── spotify_tracks.csv     # Kaggle Spotify dataset
├── static/
│   └── index.html             # Frontend
├── main.py                    # FastAPI backend
├── requirements.txt
├── Dockerfile
├── .env                       # VERTEX_PROJECT and VERTEX_LOCATION
└── .gitignore
```
 
## Running Locally
 
### Prerequisites
- Python 3.11+
- Google Cloud CLI (`gcloud`)
- A GCP project with Vertex AI API enabled
 
### Setup
 
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/music-analytics-agent.git
cd music-analytics-agent
 
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
 
# Install dependencies
pip install -r requirements.txt
pip install google-cloud-aiplatform
 
# Authenticate with GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
 
# Create .env file
echo "VERTEX_PROJECT=YOUR_PROJECT_ID" > .env
echo "VERTEX_LOCATION=us-central1" >> .env
 
# Build the database and knowledge base
python data/setup_db.py
python data/setup_rag.py
 
# Run the app
uvicorn main:app --reload --port 8000
```
 
Open http://localhost:8000 in your browser.
 
### Example Questions
- "What is the most popular genre?"
- "Compare the energy and valence of rock vs pop vs jazz"
- "Do explicit songs tend to be more popular?"
- "Which genres have the highest danceability and why?"
- "Is Drake more popular than Kendrick Lamar?"
 
## Tech Stack
- **Framework:** OpenAI Agents SDK + LiteLLM
- **Model:** Gemini 2.5 Flash via Vertex AI
- **Backend:** FastAPI + Uvicorn
- **Database:** SQLite (Spotify tracks) + ChromaDB (knowledge base)
- **Visualization:** Matplotlib
- **Deployment:** Google Cloud Run
- **Dataset:** [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) (Kaggle)