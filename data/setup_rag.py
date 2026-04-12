import chromadb
import os
import glob

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")


def split_into_sections(text):
    """Split markdown text into sections by heading."""
    sections = []
    current_section = ""
    for line in text.split("\n"):
        if line.startswith("# ") or line.startswith("## "):
            if current_section.strip():
                sections.append(current_section.strip())
            current_section = line + "\n"
        else:
            current_section += line + "\n"
    if current_section.strip():
        sections.append(current_section.strip())
    return [s for s in sections if len(s) > 20]


def setup_rag():
    # Remove existing ChromaDB to rebuild fresh
    if os.path.exists(CHROMA_DIR):
        import shutil
        shutil.rmtree(CHROMA_DIR)

    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.create_collection(
        name="music_knowledge",
        metadata={"hnsw:space": "cosine"},
    )

    documents = []
    metadatas = []
    ids = []
    doc_id = 0

    # Load all markdown files from knowledge directory
    md_files = glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md"))

    if not md_files:
        print(f"No markdown files found in {KNOWLEDGE_DIR}")
        return

    for filepath in md_files:
        filename = os.path.basename(filepath)
        print(f"Processing {filename}...")

        with open(filepath, "r") as f:
            content = f.read()

        sections = split_into_sections(content)
        print(f"  Found {len(sections)} sections")

        for section in sections:
            documents.append(section)
            metadatas.append({
                "source": filename,
                "type": "knowledge",
            })
            ids.append(f"doc_{doc_id}")
            doc_id += 1

    if not documents:
        print("No documents to add!")
        return

    # Add all documents to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"\nChromaDB created: {CHROMA_DIR}")
    print(f"  {len(md_files)} knowledge files processed")
    print(f"  {len(documents)} chunks stored")

    # Test a query
    print("\nTest query: 'What is danceability?'")
    results = collection.query(query_texts=["What is danceability?"], n_results=2)
    for i, doc in enumerate(results["documents"][0]):
        print(f"\n  Result {i + 1}:")
        print(f"  {doc[:150]}...")


if __name__ == "__main__":
    setup_rag()