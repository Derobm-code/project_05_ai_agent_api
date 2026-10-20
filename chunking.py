def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])

        if chunk:
            chunks.append(chunk)

    return chunks