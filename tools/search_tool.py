import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "spotify_tracks.db")


def search_tracks(query: str, limit: int = 10) -> str:
    """Search for tracks by name or artist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT track_id, track_name, artists, album_name,
                   popularity, tempo, key, mode, energy, danceability,
                   valence, loudness, track_genre
            FROM tracks
            WHERE track_name LIKE ? OR artists LIKE ?
            ORDER BY popularity DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": str(e)})