
from types import SimpleNamespace

import src.qa_chain as qa_chain


def test_answer_question(monkeypatch):

    # Mock retrieved document
    documents = [
        SimpleNamespace(
            page_content="Machine learning is a branch of artificial intelligence.",
            metadata={
                "source": "sample.pdf",
                "page": 1
            }
        )
    ]

    # Mock document retrieval
    monkeypatch.setattr(
        qa_chain,
        "retrieve_documents",
        lambda **kwargs: documents
    )

    # Mock Gemini response
    class FakeInteractions:

        def create(self, **kwargs):

            assert "Machine learning" in kwargs["input"]
            assert "sample.pdf" in kwargs["input"]

            return SimpleNamespace(
                output_text="Machine learning is a branch of AI. [sample.pdf, Page 1]"
            )

    class FakeClient:

        def __init__(self, **kwargs):
            self.interactions = FakeInteractions()

        def close(self):
            pass

    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

    monkeypatch.setattr(
        qa_chain.genai,
        "Client",
        FakeClient
    )

    answer = qa_chain.answer_question(
        "What is machine learning?"
    )

    assert "Machine learning" in answer
    assert "Page 1" in answer

    print("Question answering test passed!")


def test_empty_question():

    import pytest

    with pytest.raises(ValueError):
        qa_chain.answer_question("")
