import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "spotify_tracks.db")


def run_sql_query(query: str) -> str:
    """Execute a SQL query against the Spotify tracks database and return results as JSON.

    The database has one table called 'tracks' with these columns:
    - track_id (TEXT): Spotify track ID
    - artists (TEXT): Artist name(s), multiple artists separated by semicolons
    - album_name (TEXT): Album name
    - track_name (TEXT): Track name
    - popularity (INTEGER): 0-100 popularity score
    - duration_ms (INTEGER): Track duration in milliseconds
    - explicit (TEXT): 'True' or 'False'
    - danceability (REAL): 0.0-1.0
    - energy (REAL): 0.0-1.0
    - key (INTEGER): 0-11 pitch class
    - loudness (REAL): Decibels, typically -60 to 0
    - mode (INTEGER): 0=minor, 1=major
    - speechiness (REAL): 0.0-1.0
    - acousticness (REAL): 0.0-1.0
    - instrumentalness (REAL): 0.0-1.0
    - liveness (REAL): 0.0-1.0
    - valence (REAL): 0.0-1.0 (musical positiveness)
    - tempo (REAL): BPM
    - time_signature (INTEGER): Beats per bar
    - track_genre (TEXT): Genre label

    Args:
        query: A valid SQL SELECT query. Only SELECT statements are allowed.

    Returns:
        JSON string with query results (list of dicts) or error message.
    """
    # Safety: only allow SELECT queries
    stripped = query.strip().upper()
    if not stripped.startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()

        # Limit output size
        if len(results) > 100:
            return json.dumps({
                "results": results[:100],
                "total_rows": len(results),
                "note": "Showing first 100 of {} rows. Use LIMIT in your query for specific counts.".format(len(results))
            }, indent=2)

        return json.dumps({"results": results, "total_rows": len(results)}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})