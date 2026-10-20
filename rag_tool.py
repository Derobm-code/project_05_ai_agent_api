from pathlib import Path

from embeddings import get_embedding
from similarity import cosine_similarity
from chunking import chunk_text

###############################retrieval logic##################################

def load_documents(directory: str | Path) -> dict[str, str]:
    directory= Path(directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Knowledge-base directory not found: {directory}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Knowledge-base path is not a directory: {directory}"
        )

    documents = {}

    for path in sorted(directory.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()

        if text:
            documents[path.name] = text

    if not documents:
        raise ValueError(
            f"No non-empty .txt documents found in: {directory}"
        )

    return documents

def create_index(documents: dict[str, str]) -> list[dict]:
    index = []

    for filename, text in documents.items():
        chunks = chunk_text(
            text, chunk_size =100, overlap= 20,
        )

        for chunk_number, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)

            index.append(
                {
                    "filename": filename,
                    "chunk_number": chunk_number,
                    "text": chunk,
                    "embedding": embedding,
                }
            )

    return index

def search_index(
        query: str,
        index: list[dict],
        top_k: int = 3,
) -> list[dict]:

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    query_embedding = get_embedding(query)

    results = []

    for item in index:
        score = cosine_similarity(
            query_embedding,
            item["embedding"],
        )

        results.append(
            {
                "filename": item["filename"],
                "chunk_number": item["chunk_number"],
                "text": item["text"],
                "score": score,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"

RAG_INDEX = None

def get_rag_index() -> list[dict]:
    global RAG_INDEX

    if RAG_INDEX is None:
        documents = load_documents(DOCUMENTS_DIR)

        print(f"Loaded {len(documents)} documents.")
        print("Creating RAG index...")

        index = create_index(documents)

        if not index:
            raise ValueError(
                "The knowledge base did not produce a searchable index."
            )

        RAG_INDEX = index

        print(f"Created {len(RAG_INDEX)} searchable chunks.")
        print("RAG index ready.")

    return RAG_INDEX

def search_knowledge_base(query: str) -> str:
    """
    Search the local knowledge base for relevant information.
    
    Args:
        query: The user's question or search request.
        
    Returns:
        Relevant document chunks with source filenames and scores.
    """
    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be empty.")
    
    index = get_rag_index()

    results = search_index(
        query, index, top_k=3,
    )

    if not results:
        return "No relevant information was found in the knowledge base"

    output =[]

    for result in results:

        output.append(
            f"Source: {result['filename']}\n"
            f"Chunk: {result['chunk_number']}\n"
            f"Similarity: {result['score']:.4f}\n"
            f"Content: {result['text']}"
        )

    return "n\n".join(output)