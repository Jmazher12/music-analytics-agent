import chromadb
import os
import json

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")


def search_music_knowledge(query: str, n_results: int = 3) -> str:
    """Search the music knowledge base for information about audio features, genres, and analysis techniques.

    Use this tool when you need background knowledge about:
    - What Spotify audio features mean (danceability, energy, valence, etc.)
    - Genre characteristics and typical feature ranges
    - Music analysis frameworks and approaches
    - How to interpret patterns in music data

    Args:
        query: Natural language search query about music concepts.
        n_results: Number of results to return (default 3, max 5).

    Returns:
        JSON string with relevant knowledge passages and their sources.
    """
    n_results = min(n_results, 5)

    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = client.get_collection("music_knowledge")

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        passages = []
        for i in range(len(results["documents"][0])):
            passages.append({
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
            })

        return json.dumps({"results": passages}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})