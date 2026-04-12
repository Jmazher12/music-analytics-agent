from agents import Agent, function_tool
from tools.sql_tool import run_sql_query
from tools.rag_tool import search_music_knowledge


@function_tool
def query_spotify_db(query: str) -> str:
    """Execute a SQL query against the Spotify tracks database.

    The 'tracks' table has columns: track_id, artists, album_name, track_name,
    popularity, duration_ms, explicit, danceability, energy, key, loudness, mode,
    speechiness, acousticness, instrumentalness, liveness, valence, tempo,
    time_signature, track_genre.

    Only SELECT queries are allowed. Use LIMIT to avoid huge results.
    """
    return run_sql_query(query)


@function_tool
def search_knowledge(query: str) -> str:
    """Search the music knowledge base for information about audio features,
    genres, and analysis techniques. Use this to understand what audio features
    mean or how to interpret data patterns."""
    return search_music_knowledge(query)


data_agent = Agent(
    name="Data Agent",
    instructions="""You are a data collection and exploration specialist for music analytics.

Your job is to:
1. COLLECT data by writing and executing SQL queries against the Spotify database
2. EXPLORE the data by computing aggregations, comparisons, and identifying patterns

When you receive a question:
- First, search the knowledge base if you need to understand audio features or genre characteristics
- Then, write SQL queries to collect relevant data
- Compute meaningful statistics: averages, counts, rankings, comparisons
- Identify specific patterns, outliers, or trends in the data
- Always include specific numbers and data points in your findings

SQL tips:
- The table is called 'tracks'
- Use GROUP BY with AVG(), COUNT(), MIN(), MAX() for aggregations
- Use ORDER BY ... LIMIT for rankings
- Use WHERE to filter by genre, popularity range, etc.
- You can run multiple queries to explore different angles

Return your findings as a structured summary with specific data points.""",
    model="litellm/vertex_ai/gemini-2.5-flash",
    tools=[query_spotify_db, search_knowledge],
)