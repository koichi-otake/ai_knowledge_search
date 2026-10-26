from app.services.llm_service import generate_answer


def generate_search_query(question: str) -> str:
    prompt = f"""
あなたは社内文書検索用の検索クエリ生成AIです。

ユーザーの質問を、ベクトル検索用の短い検索クエリに変換してください。

ルール:
- 元の質問の意味を変えない
- 質問に含まれる重要なキーワードを維持する
- 質問にない部署名、制度、専門用語を推測で追加しない
- 検索に必要な場合のみ、一般的な同義語を少数追加する
- 日本語の検索クエリだけを返す
- 説明、箇条書き、記号を付けない
- 不要な外国語や無関係な文字列を出力しない

ユーザーの質問:
{question}
"""

    return generate_answer(prompt=prompt).strip()
