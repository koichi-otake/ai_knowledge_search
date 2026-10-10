import re

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

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # 段落が短い場合は、そのまま現在のチャンクに追加
        if len(paragraph) <= chunk_size:

            if not current_chunk:
                current_chunk = paragraph
                continue

            candidate = (
                current_chunk
                + "\n"
                + paragraph
            )

            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                chunks.append(current_chunk)

                overlap = current_chunk[-chunk_overlap:] if chunk_overlap > 0 else ""
                candidate = overlap + "\n" + paragraph if overlap else paragraph

                if len(candidate) <= chunk_size:
                    current_chunk = candidate
                else:
                    current_chunk = paragraph

            continue

        # 長い段落は「。」を優先して分割
        sentences = re.split(
            r"(?<=。)",
            paragraph,
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # 1文がchunk_size以内なら通常処理
            if len(sentence) <= chunk_size:

                if not current_chunk:
                    current_chunk = sentence
                    continue

                candidate = (
                    current_chunk
                    + "\n"
                    + sentence
                )

                if len(candidate) <= chunk_size:
                    current_chunk = candidate
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence

                continue

            # 1文が長すぎる場合は「、」を優先
            clauses = re.split(
                r"(?<=、)",
                sentence,
            )

            for clause in clauses:

                clause = clause.strip()

                if not clause:
                    continue

                # 「、」単位でもchunk_size以内なら追加
                if len(clause) <= chunk_size:

                    if not current_chunk:
                        current_chunk = clause
                        continue

                    candidate = (
                        current_chunk
                        + clause
                    )

                    if len(candidate) <= chunk_size:
                        current_chunk = candidate
                    else:
                        chunks.append(current_chunk)
                        current_chunk = clause

                    continue

                # 「、」単位でも長い場合だけ文字数で分割
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                step = chunk_size - chunk_overlap

                for start in range(
                    0,
                    len(clause),
                    step,
                ):
                    end = start + chunk_size
                    chunk = clause[start:end]

                    if chunk:
                        chunks.append(chunk)

    if current_chunk:
        chunks.append(current_chunk)



    # 最後のチャンクが小さすぎる場合は、
    # 重複部分を除いて直前のチャンクと結合する
    if len(chunks) >= 2:
        last_chunk = chunks[-1]
        previous_chunk = chunks[-2]

        minimum_chunk_size = chunk_size // 4

        overlap = (
            previous_chunk[-chunk_overlap:]
            if chunk_overlap > 0
            else ""
        )

        if overlap and last_chunk.startswith(overlap + "\n"):
            new_content = last_chunk[len(overlap) + 1:]
            combined = previous_chunk + new_content
        else:
            new_content = last_chunk
            combined = previous_chunk + "\n" + last_chunk

        if len(new_content) < minimum_chunk_size:
            if len(combined) <= chunk_size:
                chunks[-2] = combined
                chunks.pop()

    return chunks

def split_resume_words(
    words: list[dict],
) -> list[str]:

    left_words = []
    right_words = []

    for word in words:

        if word["x"] < 400:
            left_words.append(word)
        else:
            right_words.append(word)

    left_words.sort(
        key=lambda word: (
            word["y"],
            word["x"],
        )
    )

    right_words.sort(
        key=lambda word: (
            word["y"],
            word["x"],
        )
    )

    left_lines = make_lines(left_words)
    right_lines = make_lines(right_words)

    print("=== 左列の行 ===")

    for index, line in enumerate(left_lines):
        print(
            f"[{index}]",
            " | ".join(
                word["text"]
                for word in line
            )
        )

    print("=== 右列の行 ===")

    for index, line in enumerate(right_lines):
        print(
            f"[{index}]",
            " | ".join(
                word["text"]
                for word in line
            )
        )

    chunks = []

    # 学歴・職歴
    education_career = []

    for line in left_lines:
        text = " | ".join(
            word["text"]
            for word in line
        )

        if text in ["学歴", "職歴"]:
            continue

        if text == "以上":
            break

        if (
            "東京都立" in text
            or "東京工業大学" in text
            or "株式会社東芝" in text
            or "ソニーセミコンダクタ" in text
            or "一身上の都合" in text
        ):
            education_career.append(text)

    chunks.append(
        "【学歴・職歴】\n"
        + "\n".join(education_career)
    )

    # 免許・資格
    qualifications = []

    for line in right_lines:
        text = " ".join(
            word["text"]
            for word in line
        )

        if text == "以上":
            break

        if "合格" in text or "取得" in text:
            qualifications.append(text)

    chunks.append(
        "【免許・資格】\n"
        + "\n".join(qualifications)
    )

    # 自己PR
    self_pr = []

    collecting = False

    for line in right_lines:
        text = " | ".join(
            word["text"]
            for word in line
        )

        if "自己PR" in text:
            collecting = True
            continue

        if "本人希望記入欄" in text:
            break

        if collecting:
            self_pr.append(text)

    chunks.append(
        "【自己PR】\n"
        + "".join(self_pr)
    )

    # 本人希望
    preferences = []

    collecting = False

    for line in right_lines:
        text = " | ".join(
            word["text"]
            for word in line
        )

        if "本人希望記入欄" in text:
            collecting = True
            continue

        if collecting:
            preferences.append(text)

    chunks.append(
        "【本人希望】\n"
        + "\n".join(preferences)
    )

    print("=== チャンク ===")

    for index, chunk in enumerate(chunks):
        print(f"[{index}]")
        print(chunk)
        print()

    return chunks

def make_lines(
    words: list[dict],
) -> list[list[dict]]:

    lines = []

    for word in words:

        if not lines:
            lines.append([word])
            continue

        last_line = lines[-1]

        if abs(
            word["y"] - last_line[0]["y"]
        ) <= 3:
            last_line.append(word)
        else:
            lines.append([word])

    for line in lines:
        line.sort(
            key=lambda word: word["x"]
        )

    return lines

