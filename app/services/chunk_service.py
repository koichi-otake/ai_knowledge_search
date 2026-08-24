def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_sizeは1以上にしてください。")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlapは0以上にしてください。")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlapはchunk_sizeより小さくしてください。"
        )

    chunks = []

    step = chunk_size - chunk_overlap

    for start in range(
        0,
        len(text),
        step,
    ):
        end = start + chunk_size

        chunk = text[start:end]

        if not chunk:
            break

        chunks.append(chunk)

    return chunks
