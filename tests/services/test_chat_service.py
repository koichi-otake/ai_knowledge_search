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
