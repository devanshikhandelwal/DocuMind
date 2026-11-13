
from pypdf import PdfReader
from pathlib import Path


def load_pdf(file_path):
    """
    Extract text from a PDF file.
    """

    documents = []

    try:
        reader = PdfReader(file_path)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text and text.strip():

                documents.append({
                    "page_content": text.strip(),
                    "metadata": {
                        "source": Path(file_path).name,
                        "page": page_number
                    }
                })

        if not documents:
            raise ValueError(
                "No extractable text found in this PDF."
            )

        return documents

    except Exception as error:
        raise RuntimeError(
            f"Error loading PDF: {error}"
        ) from error
