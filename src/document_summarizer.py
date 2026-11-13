import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

from src.document_loader import load_pdf


def summarize_document(file_path):
    """
    Generate a comprehensive summary of an entire PDF.

    The PDF is divided into page groups to keep each
    Gemini request manageable.
    """

    # --------------------------------------------------
    # LOAD PDF CONTENT
    # --------------------------------------------------

    documents = load_pdf(file_path)

    if not documents:
        raise ValueError("No readable content found in the PDF.")

    # --------------------------------------------------
    # PREPARE PAGE GROUPS
    # --------------------------------------------------

    pages_per_group = 5
    page_groups = []

    for index in range(0, len(documents), pages_per_group):

        group = documents[index:index + pages_per_group]

        page_groups.append(group)

    # --------------------------------------------------
    # LOAD GEMINI API KEY
    # --------------------------------------------------

    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
        except (KeyError, FileNotFoundError):
            api_key = None

    if not api_key:
        raise ValueError("Gemini API key not found!")

    client = genai.Client(api_key=api_key)

    group_summaries = []

    try:

        # --------------------------------------------------
        # SUMMARIZE EACH PAGE GROUP
        # --------------------------------------------------

        for group_index, group in enumerate(page_groups, start=1):

            context = ""

            for page in group:

                page_number = page["metadata"]["page"]

                context += f"""
PAGE {page_number}

{page["page_content"]}

-----------------------------
"""

            prompt = f"""
You are DocuMind, an AI document summarization assistant.

Summarize the following PDF content accurately.

Rules:
1. Use only the provided document content.
2. Preserve important facts, names, dates and technical terms.
3. Include important headings and key points.
4. Do not invent missing information.
5. Keep the summary clear and well structured.
6. Mention the page numbers covered in this summary.

DOCUMENT CONTENT:

{context}

Write a concise but informative summary.
"""

            response = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt
            )

            summary = response.output_text

            if summary:
                group_summaries.append({
                    "group": group_index,
                    "start_page": group[0]["metadata"]["page"],
                    "end_page": group[-1]["metadata"]["page"],
                    "summary": summary
                })

        # --------------------------------------------------
        # COMBINE GROUP SUMMARIES
        # --------------------------------------------------

        combined_context = ""

        for item in group_summaries:

            combined_context += f"""
Pages {item["start_page"]}–{item["end_page"]}

{item["summary"]}

-----------------------------
"""

        final_prompt = f"""
You are DocuMind, an AI document intelligence assistant.

Create one comprehensive summary of the entire PDF
using the following section summaries.

Rules:
1. Use only the supplied summaries.
2. Preserve important information and technical details.
3. Avoid repeating the same point.
4. Organize the summary using meaningful headings.
5. Do not invent information.
6. Mention the page ranges covered.

SECTION SUMMARIES:

{combined_context}

Write the final document summary.
"""

        final_response = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=final_prompt
        )

        final_summary = final_response.output_text

        if not final_summary:
            raise RuntimeError("Gemini did not generate a final summary.")

        return {
            "summary": final_summary,
            "total_pages": len(documents),
            "sections": group_summaries
        }

    finally:
        client.close()
