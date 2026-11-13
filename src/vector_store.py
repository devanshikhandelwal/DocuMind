
from langchain_chroma import Chroma
from src.embeddings import get_embedding_model


COLLECTION_NAME = "documind_documents"


def create_vector_store(chunks, persist_directory="vector_db"):
    """
    Create or replace the ChromaDB vector store.
    """

    embedding_model = get_embedding_model()

    # Connect to the existing ChromaDB collection
    existing_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

    # Delete old records before adding new documents
    existing_store.delete_collection()

    # Create a fresh collection with the new chunks
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_name=COLLECTION_NAME
    )

    return vector_store


def load_vector_store(persist_directory="vector_db"):
    """
    Load an existing ChromaDB vector store.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

    return vector_store
