import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "spotify_tracks.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "spotify_tracks.csv")

def setup_database():
    # Remove existing DB to rebuild fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH, index_col=0)

    print(f"Loaded {len(df)} tracks")
    print(f"Columns: {list(df.columns)}")

    # Clean up data
    df = df.dropna(subset=["track_id", "track_name"])
    df = df.drop_duplicates(subset=["track_id"])

    print(f"After cleaning: {len(df)} tracks")

    # Write to SQLite
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("tracks", conn, if_exists="replace", index=False)

    # Create indexes for common queries
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_track_genre ON tracks(track_genre)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_artists ON tracks(artists)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_popularity ON tracks(popularity)")
    conn.commit()

    # Verify
    count = cursor.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
    genres = cursor.execute("SELECT COUNT(DISTINCT track_genre) FROM tracks").fetchone()[0]
    print(f"\nDatabase created: {DB_PATH}")
    print(f"  {count} tracks")
    print(f"  {genres} genres")

    # Show sample
    print("\nSample row:")
    row = cursor.execute("SELECT * FROM tracks LIMIT 1").fetchone()
    cols = [desc[0] for desc in cursor.description]
    for col, val in zip(cols, row):
        print(f"  {col}: {val}")

    conn.close()

if __name__ == "__main__":
    setup_database()