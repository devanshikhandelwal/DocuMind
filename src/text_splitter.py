
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split extracted documents into smaller chunks.

    Args:
        documents: List of extracted PDF pages.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Characters shared between chunks.

    Returns:
        List of LangChain Document objects.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for document in documents:

        split_texts = splitter.split_text(
            document["page_content"]
        )

        for text in split_texts:

            from langchain_core.documents import Document

            chunks.append(
                Document(
                    page_content=text,
                    metadata=document["metadata"]
                )
            )

    return chunks
