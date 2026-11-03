import json
import math
import re
from collections import Counter
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent / "cloud_rag_index.json"


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def load_chunks() -> list[dict]:
    with INDEX_PATH.open("r", encoding="utf-8") as file:
        index = json.load(file)

    return [
        {
            "filename": item["filename"],
            "chunk_number": item["chunk_number"],
            "text": item["text"],
        }
        for item in index
    ]


def search_cloud_knowledge_base(query: str, top_k: int = 3) -> str:
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    chunks = load_chunks()
    if not chunks:
        return "No documents found in the knowledge base."

    tokenized_chunks = [tokenize(item["text"]) for item in chunks]
    document_count = len(chunks)

    document_frequency = Counter()

    for tokens in tokenized_chunks:
        document_frequency.update(set(tokens))

    def idf(term: str) -> float:
        return math.log(
            (document_count + 1)
            / (document_frequency.get(term, 0) + 1)
        ) + 1

    def vectorize(tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        return {
            term: count * idf(term)
            for term, count in counts.items()
        }

    query_vector = vectorize(tokenize(query))
    query_norm = math.sqrt(
        sum(value * value for value in query_vector.values())
    )

    results = []

    for item, tokens in zip(chunks, tokenized_chunks):
        document_vector = vectorize(tokens)

        dot_product = sum(
            value * document_vector.get(term, 0)
            for term, value in query_vector.items()
        )

        document_norm = math.sqrt(
            sum(value * value for value in document_vector.values())
        )

        if query_norm == 0 or document_norm == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (query_norm * document_norm)

        results.append(
            {
                "filename": item["filename"],
                "chunk_number": item["chunk_number"],
                "text": item["text"],
                "score": similarity,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    relevant_results = [
        result
        for result in results
        if result["score"] > 0
    ][:top_k]

    if not relevant_results:
        return "No relevant information was found in the knowledge base."

    output = []

    for result in relevant_results:
        output.append(
            f"Source: {result['filename']}\n"
            f"Chunk: {result['chunk_number']}\n"
            f"Similarity: {result['score']:.4f}\n"
            f"Content: {result['text']}"
        )

    return "\n\n".join(output)


if __name__ == "__main__":
    print(search_cloud_knowledge_base("Python"))
