# 📚 DocuMind — AI-Powered PDF Question Answering Assistant

<p align="center">
  <b>Transform static PDF documents into an interactive AI-powered knowledge assistant.</b>
</p>

<p align="center">
  <a href="https://documinds.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Launch%20DocuMind-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Architecture-RAG-8B5CF6?style=for-the-badge" alt="RAG">
</p>

---

## 🌐 Live Application

### **Try DocuMind:** [https://documinds.streamlit.app/](https://documinds.streamlit.app/)

DocuMind is an AI-powered PDF assistant that allows users to upload PDF documents, ask questions in natural language, and receive intelligent, context-aware answers grounded in the content of their documents.

Built using **Retrieval-Augmented Generation (RAG)**, the application combines semantic search, vector embeddings, persistent vector storage, and Google's Gemini model to make document understanding more efficient and interactive.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📄 Multiple PDF Uploads | Upload and process multiple PDF documents in one workspace. |
| 📝 Text Extraction | Extract text from PDF pages using PyPDF while preserving page metadata. |
| 🧩 Intelligent Chunking | Split extracted text into overlapping chunks for effective retrieval. |
| 🧠 Semantic Embeddings | Convert text chunks into vector representations using Sentence Transformers. |
| 🗄️ Vector Database | Store document embeddings and metadata using ChromaDB. |
| 🔍 Semantic Search | Retrieve relevant document passages based on the user's question. |
| 🤖 AI Question Answering | Generate context-aware answers using Google Gemini. |
| 📚 Source Citations | Display source document names, page numbers, and retrieved text passages. |
| 💬 Conversational Memory | Support follow-up questions using recent conversation history and question rewriting. |
| 📖 Full Document Summarization | Generate a comprehensive summary of an entire PDF. |
| 📑 Section-wise Summaries | Summarize document sections in groups of five pages and combine them into a final summary. |
| 🎯 Document-Specific Retrieval | Restrict retrieval to the currently selected PDF. |

---

## 🧠 System Architecture

DocuMind uses a Retrieval-Augmented Generation pipeline to provide answers based on uploaded documents instead of relying only on the language model's general knowledge.

### RAG Workflow

```mermaid
flowchart TD
    A["📄 PDF Upload"] --> B["Text Extraction using PyPDF"]
    B --> C["Recursive Text Chunking"]
    C --> D["Hugging Face Embeddings"]
    D --> E[("ChromaDB Vector Store")]

    F["User Question"] --> G["Question Rewriting"]
    G --> H["Semantic Retrieval"]
    E --> H
    H --> I["Relevant Document Chunks"]
    I --> J["Google Gemini"]
    J --> K["Context-Aware Answer"]
    K --> L["Source Citations and Page References"]
    L --> M["Streamlit Interface"]
```

### Document Summarization Workflow

```mermaid
flowchart TD
    A["Uploaded PDF"] --> B["Extract Page Text"]
    B --> C["Group Pages in Batches of Five"]
    C --> D["Generate Section Summaries using Gemini"]
    D --> E["Combine Section Summaries"]
    E --> F["Generate Final Document Summary"]
    F --> G["Display Summary and Section-wise Results"]
```

---

## ⚙️ Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Core application development |
| Frontend | Streamlit | Interactive web application |
| LLM | Google Gemini 3.5 Flash Lite | Question answering and summarization |
| AI Architecture | Retrieval-Augmented Generation | Grounded document question answering |
| Embedding Model | all-MiniLM-L6-v2 | Semantic text embeddings |
| Embedding Framework | Sentence Transformers | Generate vector representations |
| Vector Database | ChromaDB | Persistent vector storage and similarity search |
| PDF Processing | PyPDF | Extract text from PDF documents |
| AI Framework | LangChain | Document splitting and embedding integrations |
| Environment Management | Python Virtual Environment | Dependency isolation |
| Testing | Pytest | Automated testing |
| Deployment | Streamlit Community Cloud | Public application hosting |

---

## 🔄 How DocuMind Works

### 1. Document Ingestion
- Users upload one or multiple PDF files.
- PyPDF extracts text from individual pages.
- Page numbers and source filenames are retained as metadata.

### 2. Text Processing
- Extracted text is divided into smaller chunks.
- Recursive Character Text Splitter is used.
- Chunk size: **1000 characters**
- Chunk overlap: **200 characters**

This helps preserve context between neighboring chunks.

### 3. Embedding Generation
- The `sentence-transformers/all-MiniLM-L6-v2` model generates 