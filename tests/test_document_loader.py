
from src.text_splitter import split_documents


def test_text_splitting():

    documents = [
        {
            "page_content": (
                "Machine learning is a branch of AI. " * 100
            ),
            "metadata": {
                "source": "sample.pdf",
                "page": 1
            }
        }
    ]

    chunks = split_documents(
        documents,
        chunk_size=200,
        chunk_overlap=50
    )

    assert len(chunks) > 1

    assert all(len(chunk.page_content) <= 200 for chunk in chunks)

    assert chunks[0].metadata["page"] == 1

    print("Text splitting test passed!")
