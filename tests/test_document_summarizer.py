
from unittest.mock import patch, MagicMock

from src.document_summarizer import summarize_document


def test_document_summarizer():

    mock_documents = [
        {
            "page_content": f"This is sample content from page {i}.",
            "metadata": {
                "source": "sample.pdf",
                "page": i
            }
        }
        for i in range(1, 8)
    ]

    mock_client = MagicMock()

    mock_client.interactions.create.side_effect = [
        MagicMock(output_text="Summary of pages 1 to 5."),
        MagicMock(output_text="Summary of pages 6 to 7."),
        MagicMock(output_text="Complete document summary.")
    ]

    with patch(
        "src.document_summarizer.load_pdf",
        return_value=mock_documents
    ), patch(
        "src.document_summarizer.genai.Client",
        return_value=mock_client
    ), patch(
        "src.document_summarizer.load_dotenv"
    ), patch.dict(
        "os.environ",
        {"GOOGLE_API_KEY": "test-key"}
    ):

        result = summarize_document("sample.pdf")

    assert result["total_pages"] == 7

    assert result["summary"] == "Complete document summary."

    assert len(result["sections"]) == 2

    assert result["sections"][0]["start_page"] == 1

    assert result["sections"][1]["end_page"] == 7

    assert mock_client.interactions.create.call_count == 3

    mock_client.close.assert_called_once()


def test_empty_document():

    with patch(
        "src.document_summarizer.load_pdf",
        return_value=[]
    ):

        try:
            summarize_document("empty.pdf")
            assert False, "Expected ValueError"

        except ValueError as error:
            assert "No readable content" in str(error)
