from fastapi.testclient import TestClient

from app.main import app

import app.services.chat_service as chat_service


client = TestClient(app)


def test_chat_api(
    monkeypatch,
):

    def fake_ask(
        db,
        question,
    ):
        return {
            "question": question,
            "answer": "テスト回答",
            "sources": [],
        }

    monkeypatch.setattr(
        chat_service,
        "ask",
        fake_ask,
    )

    response = client.post(
        "/chat",
        json={
            "question": "有給休暇は？"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["answer"] == "テスト回答"
