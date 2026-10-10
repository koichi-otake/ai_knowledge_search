import pytest

from app.services.chunk_service import split_text


def test_empty_text_returns_empty_list():
    assert split_text("") == []


def test_short_text_returns_one_chunk():
    assert split_text("これはテストです。") == ["これはテストです。"]


def test_short_paragraphs_are_combined():
    result = split_text(
        "最初の段落です。\n次の段落です。",
        chunk_size=30,
        chunk_overlap=5,
    )

    assert len(result) == 1
    assert "最初の段落です。" in result[0]
    assert "次の段落です。" in result[0]


def test_invalid_chunk_size_raises_error():
    with pytest.raises(ValueError):
        split_text("テスト", chunk_size=0)


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        split_text(
            "テスト",
            chunk_size=10,
            chunk_overlap=10,
        )

def test_long_text_is_split_into_chunks():
    text = "あ" * 120

    result = split_text(
        text,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(result) > 1
    assert all(len(chunk) <= 50 for chunk in result)


def test_short_last_chunk_is_merged():
    text = "あ" * 45 + "\n" + "い" * 5

    result = split_text(
        text,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(result) == 1
    assert "あ" * 45 in result[0]
    assert "い" * 5 in result[0]

def test_long_clause_chunks_overlap():
    text = "あ" * 120

    result = split_text(
        text,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(result) >= 2

    # 連続するチャンクの末尾・先頭に10文字の重複がある
    for previous, current in zip(result, result[1:]):
        assert previous[-10:] == current[:10]

def test_paragraph_chunks_preserve_context_overlap():
    text = "あ" * 40 + "\n" + "い" * 40

    result = split_text(
        text,
        chunk_size=51,
        chunk_overlap=10,
    )

    assert len(result) == 2
    assert result[0].endswith("あ" * 10)
    assert result[1].startswith("あ" * 10)
