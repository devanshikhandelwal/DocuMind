
import streamlit as st
import base64
import tempfile
import os

from src.document_loader import load_pdf
from src.text_splitter import split_documents
from src.vector_store import create_vector_store
from src.qa_chain import answer_question
from src.document_summarizer import summarize_document

def display_pdf(pdf_bytes, height=750):
    """Display a PDF inside the Streamlit application."""

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="{height}"
            type="application/pdf"
            style="border: none; border-radius: 12px;"
        ></iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)
# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="DocuMind | AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0b1020 0%,
        #11152b 50%,
        #17112c 100%
    );
    color: #f1f5f9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #15172b,
        #101426
    );
    border-right: 1px solid rgba(139, 92, 246, 0.2);
}

section[data-testid="stSidebar"] h2 {
    color: #ffffff;
}

.hero {
    background: linear-gradient(
        120deg,
        #6d28d9,
        #7c3aed,
        #2563eb
    );
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(109, 40, 217, 0.25);
}

.hero h1 {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1.5px;
}

.hero p {
    color: #e9d5ff;
    font-size: 16px;
    margin-top: 10px;
}

.section-heading {
    font-size: 21px;
    font-weight: 700;
    color: #f8fafc;
    margin: 22px 0 12px 0;
}

.metric-card {
    background: rgba(30, 41, 70, 0.75);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 16px;
    padding: 20px;
    min-height: 115px;
}

.metric-label {
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}

.upload-card {
    background: rgba(30, 41, 70, 0.55);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 18px;
    padding: 22px;
    margin: 15px 0;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 11px;
    padding: 11px 20px;
    font-weight: 700;
    transition: 0.25s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #8b5cf6, #6366f1);
    color: white;
    border: none;
    box-shadow: 0 5px 20px rgba(124, 58, 237, 0.35);
    transform: translateY(-2px);
}

.stChatInput textarea {
    background: #1e2540 !important;
    color: white !important;
    border: 1px solid #6650b8 !important;
    border-radius: 14px !important;
}

[data-testid="stChatMessage"] {
    background: rgba(30, 41, 70, 0.65);
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stFileUploader"] {
    background: rgba(30, 41, 70, 0.45);
    border-radius: 14px;
    padding: 12px;
}

hr {
    border-color: rgba(139, 92, 246, 0.2);
}

.small-muted {
    color: #94a3b8;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

if "processed_signature" not in st.session_state:
    st.session_state.processed_signature = None

if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = {}
if "document_summaries" not in st.session_state:
    st.session_state.document_summaries = {}
# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 0 22px 0;">
        <div style="font-size: 29px; font-weight: 800;">
            📚 DocuMind
        </div>
        <div style="color: #a5b4fc; font-size: 13px;">
            AI-powered document intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📂 Your Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or multiple PDF files."
    )

    current_signature = tuple(
        (file.name, file.size)
        for file in uploaded_files
    ) if uploaded_files else None

    if current_signature != st.session_state.processed_signature:
        st.session_state.documents_processed = False

    st.caption("PDF files only • Multiple uploads supported")

    process_button = st.button(
        "⚡ Process Documents",
        use_container_width=True
    )

    if process_button:

        if not uploaded_files:
            st.warning("Please upload at least one PDF.")

        else:

            all_chunks = []
            successful_files = []
            failed_files = []

            progress = st.progress(0)
            status = st.empty()

            for index, uploaded_file in enumerate(uploaded_files):

                status.info(
                    f"Processing {uploaded_file.name}..."
                )

                temp_path = None

                try:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(uploaded_file.getvalue())
                        temp_path = temp_file.name

                    documents = load_pdf(temp_path)
                    st.session_state.pdf_files[uploaded_file.name] = (
                        uploaded_file.getvalue()
                    )

                    for document in documents:
                        document["metadata"]["source"] = uploaded_file.name

                    chunks = split_documents(documents)

                    if not chunks:
                        raise ValueError("No readable text found.")

                    all_chunks.extend(chunks)
                    successful_files.append(uploaded_file.name)

                except Exception as error:

                    failed_files.append(
                        (uploaded_file.name, str(error))
                    )

                finally:

                    if temp_path and os.path.exists(temp_path):
                        os.unlink(temp_path)

                progress.progress(
                    (index + 1) / len(uploaded_files)
                )

            if all_chunks:

                try:

                    create_vector_store(
                        all_chunks,
                        persist_directory="vector_db"
                    )

                    st.session_state.documents_processed = True
                    st.session_state.processed_files = successful_files
                    st.session_state.total_chunks = len(all_chunks)
                    st.session_state.processed_signature = current_signature

                    st.session_state.messages = []
                    st.session_state.document_summaries = {}

                    status.success("Document processing complete!")

                    st.success(
                        f"Successfully processed {len(successful_files)} PDF(s) "
                        f"and created {len(all_chunks)} chunks!"
                    )

                except Exception as error:

                    st.session_state.documents_processed = False
                    status.error(f"Vector database error: {error}")

            else:

                st.session_state.documents_processed = False
                status.error("No documents could be processed.")

            if failed_files:

                with st.expander("⚠️ Files that could not be processed"):

                    for filename, error in failed_files:
                        st.write(f"**{filename}**: {error}")

    st.divider()

    st.markdown("### 📊 Workspace Status")

    if st.session_state.documents_processed:

        st.markdown("""
        <div style="
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.4);
            border-radius: 12px;
            padding: 13px;
        ">
            <span style="color: #34d399; font-weight: 700;">
                ● Documents Ready
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            f"{len(st.session_state.processed_files)} documents indexed"
        )

    else:

        st.markdown("""
        <div style="
            background: rgba(245, 158, 11, 0.10);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 12px;
            padding: 13px;
        ">
            <span style="color: #fbbf24; font-weight: 700;">
                ● Awaiting Documents
            </span>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.processed_files:

        with st.expander("View indexed documents"):

            for filename in st.session_state.processed_files:
                st.write(f"📄 {filename}")



# ==================================================
# MAIN HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">
    <h1>📚 DocuMind</h1>
    <p>Your documents. Your knowledge. One intelligent AI assistant.</p>
    <div style="display:inline-block;background:rgba(255,255,255,0.16);padding:7px 13px;border-radius:20px;color:white;font-size:12px;margin-top:8px;">
        ✨ POWERED BY RAG + GEMINI AI
    </div>
</div>
""", unsafe_allow_html=True)




# ==================================================
# METRIC CARDS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📄 DOCUMENTS INDEXED</div>
        <div class="metric-value">
            {len(st.session_state.processed_files)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🧩 TOTAL CHUNKS</div>
        <div class="metric-value">
            {st.session_state.total_chunks}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    status_text = (
        "Ready"
        if st.session_state.documents_processed
        else "Not Ready"
    )

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🤖 AI ASSISTANT</div>
        <div class="metric-value" style="font-size: 23px;">
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)



# ==================================================
# SPLIT-SCREEN DOCUMENT WORKSPACE
# ==================================================

st.markdown(
    '<div class="section-heading">💬 Your AI Document Workspace</div>',
    unsafe_allow_html=True
)

if not st.session_state.documents_processed:

    st.info(
        "👈 Upload and process your PDF documents "
        "to open the document workspace."
    )

    st.markdown("### ✨ What can DocuMind do?")

    st.markdown("""
    - 📄 Summarize lengthy PDF documents
    - 🔍 Find specific information instantly
    - 🤖 Ask questions using document context
    - 📚 Explore retrieved sources and page references
    """)

else:

    # Get available PDF files
    available_files = st.session_state.processed_files

    if not available_files:
        st.warning("No processed documents are available.")

    else:

        # --------------------------------------------------
        # DOCUMENT SELECTION
        # --------------------------------------------------

        st.markdown("### 📂 Select a document")

        selected_pdf = st.selectbox(
            "Choose a PDF to preview",
            options=available_files,
            key="selected_pdf"
        )

        pdf_bytes = st.session_state.pdf_files.get(selected_pdf)

        # --------------------------------------------------
        # DOCUMENT SUMMARIZATION
        # --------------------------------------------------

        st.markdown("### ✨ Full Document Summarization")

        st.caption(
            "Generate an AI-powered summary of the entire selected PDF."
        )

        if st.button(
            "✨ Generate Full Document Summary",
            use_container_width=True,
            key="generate_summary"
        ):
            pdf_data = st.session_state.pdf_files.get(selected_pdf)

            if not pdf_data:
                st.error("PDF file not found. Please upload it again.")
            else:
                temp_path = None

                try:
                    with st.spinner(
                        "📖 Reading document and generating summary..."
                    ):
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".pdf"
                        ) as temp_file:
                            temp_file.write(pdf_data)
                            temp_path = temp_file.name

                        result = summarize_document(temp_path)

                        st.session_state.document_summaries[
                            selected_pdf
                        ] = result

                except Exception as error:
                    st.error(f"Summary generation failed: {error}")

                finally:
                    if temp_path and os.path.exists(temp_path):
                        os.unlink(temp_path)

        # Display previously generated summary
        summary_result = st.session_state.document_summaries.get(
            selected_pdf
        )

        if summary_result:
            st.markdown("#### 📝 Complete Document Summary")

            st.markdown(summary_result["summary"])

            st.caption(
                f"Summary generated from "
                f"{summary_result['total_pages']} text-containing pages."
            )

            with st.expander("📚 View Section-wise Summaries"):
                for section in summary_result["sections"]:
                    st.markdown(
                        f"**Pages {section['start_page']}–"
                        f"{section['end_page']}**"
                    )

                    st.write(section["summary"])
                    st.divider()


        # --------------------------------------------------
        # TWO-COLUMN LAYOUT
        # --------------------------------------------------

        pdf_column, chat_column = st.columns(
            [1, 1],
            gap="large"
        )

        # ==================================================
        # LEFT SIDE - PDF VIEWER
        # ==================================================

        with pdf_column:

            st.markdown("### 📄 Document Preview")

            if pdf_bytes:

                st.caption(f"Currently viewing: {selected_pdf}")

                display_pdf(
                    pdf_bytes,
                    height=750
                )

            else:

                st.warning(
                    "PDF preview unavailable. "
                    "Please upload and process this document again."
                )

        # ==================================================
        # RIGHT SIDE - AI CHAT
        # ==================================================

        with chat_column:

            st.markdown("### 🤖 Chat with DocuMind")

            st.caption(
                "Ask questions about your uploaded documents."
            )

            # Clear chat button
            if st.button(
                "🗑️ Clear Chat",
                use_container_width=False
            ):
                st.session_state.messages = []
                st.rerun()

            # --------------------------------------------------
            # DISPLAY CHAT HISTORY
            # --------------------------------------------------

            chat_container = st.container(height=570)

            with chat_container:

                for message in st.session_state.messages:

                    with st.chat_message(message["role"]):

                        st.markdown(message["content"])

                        if (
                            message["role"] == "assistant"
                            and message.get("sources")
                        ):

                            st.markdown("**📚 Sources used**")

                            for source in message["sources"]:

                                with st.expander(
                                    f"📄 {source['source']} | "
                                    f"Page {source['page']}"
                                ):

                                    st.markdown(
                                        "**Retrieved text preview**"
                                    )

                                    content = source["content"]

                                    preview = content[:700]

                                    if len(content) > 700:
                                        preview += "..."

                                    st.write(preview)

            # --------------------------------------------------
            # SUGGESTED QUESTIONS
            # --------------------------------------------------

            st.markdown("**✨ Try asking**")

            suggestion_columns = st.columns(2)

            suggestions = [
                "Summarize this document",
                "What are the main topics?",
                "Explain the important concepts",
                "What are the key takeaways?"
            ]

            for index, suggestion in enumerate(suggestions):

                with suggestion_columns[index % 2]:

                    if st.button(
                        suggestion,
                        key=f"suggestion_{index}",
                        use_container_width=True
                    ):

                        st.session_state.pending_question = suggestion
                        st.rerun()

            # --------------------------------------------------
            # QUESTION INPUT
            # --------------------------------------------------

            typed_question = st.chat_input(
                "Ask anything about your documents..."
            )

            pending_question = st.session_state.pop(
                "pending_question",
                None
            )

            prompt = typed_question or pending_question

            if prompt:

                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })

                with chat_container:

                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):

                        with st.spinner(
                            "🔍 Searching your documents..."
                        ):

                            try:

                                result = answer_question(
                                prompt,
                                return_sources=True,
                                chat_history=st.session_state.messages[:-1],
                                source=selected_pdf
                                )

                                answer = result["answer"]
                                sources = result["sources"]

                                st.markdown(answer)

                                if sources:

                                    st.markdown("**📚 Sources used**")

                                    for source in sources:

                                        with st.expander(
                                            f"📄 {source['source']} | "
                                            f"Page {source['page']}"
                                        ):

                                            content = source["content"]

                                            preview = content[:700]

                                            if len(content) > 700:
                                                preview += "..."

                                            st.write(preview)

                                else:

                                    st.caption(
                                        "No relevant source passages were retrieved."
                                    )

                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": answer,
                                    "sources": sources
                                })

                            except Exception as error:

                                st.error(
                                    f"Unable to generate answer: {error}"
                                )



