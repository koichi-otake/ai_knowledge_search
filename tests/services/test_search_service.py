import pytest
import app.services.search_service as search_service


def test_search_filters_by_similarity(monkeypatch):

    class FakeRow:
        def __init__(self, distance, id=1, document_id=1):
            self.distance = distance
            self.id = id
            self.document_id = document_id
        
    fake_rows = [
        FakeRow(0.2),   # similarity = 0.8 → 採用
        FakeRow(0.549999),  # similarity ≒ 0.450001 → 採用
        FakeRow(0.7),   # similarity = 0.3 → 除外
    ]

    def fake_create_embedding(question):
        return [0.1, 0.2]

    def fake_search_by_embedding(db, embedding, limit):
        return fake_rows

    monkeypatch.setattr(
        search_service,
        "create_embedding",
        fake_create_embedding,
    )

    monkeypatch.setattr(
        search_service,
        "search_by_embedding",
        fake_search_by_embedding,
    )

    result = search_service.search(
        db=None,
        question="テスト",
        limit=5,
    )

    assert len(result) == 2
    assert result[0]["similarity"] == pytest.approx(0.8)
    assert result[1]["similarity"] == pytest.approx(0.450001)
