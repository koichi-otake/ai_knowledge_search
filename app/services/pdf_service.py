import fitz


def extract_text(
    pdf_path: str,
) -> str:

    document = fitz.open(pdf_path)

    texts = []

    for page in document:

        texts.append(
            page.get_text()
        )

    document.close()

    return "\n".join(texts)
