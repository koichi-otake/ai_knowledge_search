import app.services.chat_service as chat_service


def test_no_document_does_not_call_llm(
    monkeypatch,
):

    called = False

    def fake_search(
        db,
        question,
        limit,
    ):
        return []

    def fake_generate_answer(
        prompt,
    ):
        nonlocal called
        called = True
        return "dummy"

    monkeypatch.setattr(
        chat_service,
        "search",
        fake_search,
    )

    monkeypatch.setattr(
        chat_service,
        "generate_answer",
        fake_generate_answer,
    )

    result = chat_service.ask(
        db=None,
        question="テスト",
    )

    assert called is False

    assert (
        result["answer"]
        ==
        "社内文書から回答を確認できませんでした。担当部署へお問い合わせください。"
    )

def test_no_document_returns_no_answer(monkeypatch):
    def fake_search(db, question, limit):
        return []

    def fake_generate_answer(prompt):
        raise AssertionError("関連文書がない場合、LLMは呼び出してはいけない")

    monkeypatch.setattr(chat_service, "search", fake_search)
    monkeypatch.setattr(chat_service, "generate_answer", fake_generate_answer)

    result = chat_service.ask(
        db=None,
        question="東京タワーの高さは何メートルですか？",
    )

    assert result["question"] == "東京タワーの高さは何メートルですか？"
    assert result["answer"] == chat_service.NO_ANSWER_MESSAGE
    assert result["sources"] == []


def test_related_document_calls_llm(monkeypatch):
    class FakeChunk:
        document_id = 1
        id = 10
        chunk_index = 0
        content = "有給休暇は入社6か月後に10日付与されます。"

    fake_results = [
        {
            "chunk": FakeChunk(),
            "distance": 0.2,
            "similarity": 0.8,
        }
    ]

    def fake_search(db, question, limit):
        return fake_results

    def fake_build_rag_prompt(question, contexts):
        assert question == "有給休暇はいつ付与されますか？"
        assert contexts == [
            "有給休暇は入社6か月後に10日付与されます。"
        ]
        return "テスト用プロンプト"

    def fake_generate_answer(prompt):
        assert prompt == "テスト用プロンプト"
        return "入社6か月後に10日付与されます。"

    monkeypatch.setattr(chat_service, "search", fake_search)
    monkeypatch.setattr(
        chat_service,
        "build_rag_prompt",
        fake_build_rag_prompt,
    )
    monkeypatch.setattr(
        chat_service,
        "generate_answer",
        fake_generate_answer,
    )

    result = chat_service.ask(
        db=None,
        question="有給休暇はいつ付与されますか？",
    )

    assert result["question"] == "有給休暇はいつ付与されますか？"
    assert result["answer"] == "入社6か月後に10日付与されます。"

    assert result["sources"] == [
        {
            "document_id": 1,
            "chunk_id": 10,
            "chunk_index": 0,
            "similarity": 0.8,
        }
    ]
