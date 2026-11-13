
from src.vector_store import create_vector_store
from src.retriever import retrieve_documents
from langchain_core.documents import Document


def test_document_retrieval(tmp_path):

    documents = [
        Document(
            page_content="Machine learning is a branch of artificial intelligence.",
            metadata={"source": "sample.pdf", "page": 1}
        ),
        Document(
            page_content="Python is used for programming and software development.",
            metadata={"source": "sample.pdf", "page": 2}
        ),
        Document(
            page_content="Deep learning uses neural networks.",
            metadata={"source": "sample.pdf", "page": 3}
        )
    ]

    create_vector_store(
        documents,
        persist_directory=str(tmp_path)
    )

    results = retrieve_documents(
        query="What is machine learning?",
        persist_directory=str(tmp_path),
        k=2
    )

    assert len(results) == 2

    assert any(
        "machine learning" in doc.page_content.lower()
        for doc in results
    )

    assert results[0].metadata["source"] == "sample.pdf"

    print("Document retrieval test passed!")
