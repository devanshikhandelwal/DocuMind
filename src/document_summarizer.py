
import os
import streamlit as st

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.document_loader import load_pdf


def summarize_document(file_path):
    """
    Generate a comprehensive summary of an entire PDF.

    The document is divided into groups of five pages.
    Each group is summarized separately, and the summaries
    are combined into one final document summary.
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

    total_groups = len(page_groups)

    # --------------------------------------------------
    # LOAD GEMINI API KEY
    # --------------------------------------------------

    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Check Streamlit Secrets."
        )

    # --------------------------------------------------
    # INITIALIZE GEMINI CLIENT
    # --------------------------------------------------

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000)
    )

    group_summaries = []

    progress = st.progress(0)
    status = st.empty()

    try:

        # --------------------------------------------------
        # SUMMARIZE EACH PAGE GROUP
        # --------------------------------------------------

        for group_index, group in enumerate(page_groups, start=1):

            start_page = group[0]["metadata"]["page"]
            end_page = group[-1]["metadata"]["page"]

            status.info(
                f"Generating summary for pages "
                f"{start_page}-{end_page} "
                f"(group {group_index} of {total_groups})..."
            )

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
6. Mention the page numbers covered.

DOCUMENT CONTENT:

{context}

Write a concise but informative summary.
"""

            response = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt
            )

            summary = response.output_text

            if not summary:
                raise RuntimeError(
                    f"Gemini returned an empty summary for "
                    f"pages {start_page}-{end_page}."
                )

            group_summaries.append({
                "group": group_index,
                "start_page": start_page,
                "end_page": end_page,
                "summary": summary
            })

            progress.progress(
                group_index / (total_groups + 1)
            )

        # --------------------------------------------------
        # COMBINE GROUP SUMMARIES
        # --------------------------------------------------

        status.info("Combining section summaries into the final summary...")

        combined_context = ""

        for item in group_summaries:
            combined_context += f"""
Pages {item["start_page"]}-{item["end_page"]}

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
            raise RuntimeError(
                "Gemini did not generate a final summary."
            )

        progress.progress(1.0)
        status.success("Document summary generated successfully!")

        return {
            "summary": final_summary,
            "total_pages": len(documents),
            "sections": group_summaries
        }

    finally:
        client.close()
