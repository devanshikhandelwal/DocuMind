
from src.vector_store import load_vector_store


def retrieve_documents(
    query,
    persist_directory="vector_db",
    k=3,
    page=None,
    source=None
):
    """
    Retrieve relevant document chunks.

    Supports:
    - Global document search
    - PDF-specific search
    - Page-specific search
    - PDF and page-specific search together
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    vector_store = load_vector_store(
        persist_directory=persist_directory
    )

    # Build metadata filters
    filters = []

    if source is not None:
        filters.append({"source": source})

    if page is not None:
        filters.append({"page": page})

    # Combine filters when both are provided
    if len(filters) == 2:
        metadata_filter = {"$and": filters}
    elif len(filters) == 1:
        metadata_filter = filters[0]
    else:
        metadata_filter = None

    # Retrieve matching chunks
    if metadata_filter:
        results = vector_store.similarity_search(
            query,
            k=k,
            filter=metadata_filter
        )
    else:
        results = vector_store.similarity_search(
            query,
            k=k
        )

    return results
