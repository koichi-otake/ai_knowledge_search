import re

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

def extract_words(
    pdf_path: str,
) -> list[dict]:

    document = fitz.open(pdf_path)

    words = []

    for page_index, page in enumerate(document):

        for word in page.get_text("words"):

            x0, y0, x1, y1, text, block_no, line_no, word_no = word

            words.append(
                {
                    "page": page_index,
                    "x": x0,
                    "y": y0,
                    "text": text,
                    "block_no": block_no,
                    "line_no": line_no,
                    "word_no": word_no,
                }
            )

    document.close()

    return words

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def is_resume_document(text: str) -> bool:
    normalized_text = normalize_text(text)

    markers = [
        "履歴書",
        "学歴・職歴",
        "免許・資格",
        "本人希望記入欄",
    ]

    matched_count = sum(
        marker in normalized_text
        for marker in markers
    )

    return matched_count >= 2
