def build_rag_prompt(
    question: str,
    contexts: list[str],
) -> str:
    context_text = "\n\n---\n\n".join(contexts)

    return f"""
あなたは社内文書検索AIです。

以下の社内文書だけを根拠として回答してください。
文書から回答を確認できない場合は、
「社内文書から回答を確認できませんでした。」
と回答してください。

【社内文書】
{context_text}

【質問】
{question}

【回答】
""".strip()
