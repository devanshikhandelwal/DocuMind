# 📚 DocuMind — AI-Powered PDF Q&A Assistant

**Chat with your PDFs. Understand documents. Find answers intelligently.**

DocuMind is an AI-powered document intelligence application that allows users to upload PDF documents, ask questions in natural language, and receive context-aware answers using Retrieval-Augmented Generation (RAG).

Built with Python, Streamlit, Gemini, HuggingFace embeddings, and ChromaDB.

---

## ✨ Features

### 📄 Document Processing
- Upload multiple PDF documents.
- Extract text from PDF pages.
- Split documents into smaller, meaningful chunks.
- Preserve document filenames and page metadata.

### 🔍 Intelligent Search
- Generate vector embeddings using HuggingFace Sentence Transformers.
- Store document embeddings in ChromaDB.
- Perform semantic similarity search.
- Retrieve relevant document passages for answering questions.

### 🤖 AI-Powered Question Answering
- Ask questions about uploaded PDFs using natural language.
- Generate context-aware answers using Google's Gemini API.
- Chat with a selected PDF instead of searching all documents.
- Ask questions about specific PDF pages.
- Maintain conversational context for follow-up questions.

### 📝 Document Summarization
- Generate full-document summaries.
- Process documents in page groups.
- Combine section summaries into a final summary.
- View section-wise summaries with page ranges.

### 📚 Source References
- Display source PDF filenames.
- Show relevant page numbers.
- Preview retrieved document passages.

### 🎨 Interactive Interface
- Built with Streamlit.
- Split-screen PDF viewer and AI chat workspace.
- Multiple PDF upload support.
- Document processing status and metrics.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| LangChain | Document processing and retrieval components |
| Google Gemini API | Question answering and summarization |
| HuggingFace Sentence Transformers | Text embeddings |
| ChromaDB | Vector database |
| PyPDF | PDF text extraction |
| Pytest | Automated testing |
| python-dotenv | Environment variable management |

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`

**LLM:** `gemini-3.5-flash-lite`

---

## 🏗️ Project Architecture

DocuMind follows a Retrieval-Augmented Generation architecture.

1. Users upload PDF documents.
2. Text is extracted and divided into chunks.
3. HuggingFace generates vector embeddings.
4. ChromaDB stores the embeddings and document metadata.
5. A user submits a question.
6. The retriever finds relevant document chunks.
7. Gemini generates an answer using the retrieved context.
8. The application displays the answer along with source references.

---

## 📁 Project Structure

```text
DocuMind/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── document_summarizer.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── qa_chain.py
│
├── tests/
│   ├── __init__.py
│   ├── test_document_loader.py
│   ├── test_document_summarizer.py
│   ├── test_embeddings.py
│   ├── test_vector_store.py
│   ├── test_retriever.py
│   ├── test_text_splitter.py
│   └── test_qa_chain.py
│
├── data/
│   └── uploaded_docs/
│
└── vector_db/
```

Generated files and local data such as `.env`, uploaded PDFs, and the vector database should remain excluded from Git.

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd DocuMind
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Obtain your API key through Google AI Studio.

**Important:** Never upload your actual `.env` file or API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Running Tests

DocuMind includes automated tests for its main modules.

Run the complete test suite:

```bash
pytest -v
```

### Current Test Results

| Module | Tests |
|---|---:|
| Document loader | 1 |
| Document summarizer | 2 |
| Embeddings | 1 |
| QA chain | 2 |
| Retriever | 1 |
| Text splitter | 1 |
| Vector store | 1 |
| **Total** | **9 passed** |

---

## 🧠 Core Concepts Demonstrated

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Semantic search
- Text embeddings
- Vector databases
- Document preprocessing
