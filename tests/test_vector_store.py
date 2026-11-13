
from src.vector_store import create_vector_store


def test_vector_store_creation(tmp_path):

    chunks = [
        {
            "page_content": "Machine learning is a branch of artificial intelligence.",
            "metadata": {"source": "sample.pdf", "page": 1}
        },
        {
            "page_content": "Python is a popular programming language.",
            "metadata": {"source": "sample.pdf", "page": 2}
        }
    ]

    from langchain_core.documents import Document

    documents = [
        Document(
            page_content=chunk["page_content"],
            metadata=chunk["metadata"]
        )
        for chunk in chunks
    ]

    vector_store = create_vector_store(
        documents,
        persist_directory=str(tmp_path)
    )

    results = vector_store.similarity_search(
        "What is machine learning?",
        k=1
    )

    assert len(results) == 1

    assert "machine learning" in results[0].page_content.lower()

    print("Vector store test passed!")
