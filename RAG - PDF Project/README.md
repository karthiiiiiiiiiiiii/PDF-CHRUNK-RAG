# 📄 RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) based PDF Question Answering System built using Python, Streamlit, FAISS, Sentence Transformers, and Ollama.

The application allows users to upload PDF documents, process them into semantic chunks, store embeddings in a FAISS vector database, and ask questions based on the uploaded PDF content.

---

## 🚀 Features

- Upload PDF documents
- Extract text from PDF files
- Semantic text chunking
- Generate embeddings using Sentence Transformers
- Store embeddings in FAISS vector database
- Retrieve relevant content using similarity search
- Generate answers using Ollama (Llama 3)
- Streamlit-based user interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- FAISS
- Sentence Transformers
- PyMuPDF (fitz)
- Ollama
- NumPy

---

## 📂 Project Structure

```text
RAG-PDF-Chatbot/
│
├── app.py
├── pdf_processor.py
├── chunker.py
├── embeddings.py
├── retriever.py
├── llm.py
├── chunks.pkl
├── faiss_index.pkl
├── data/
│   └── sample.pdf
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/rag-pdf-chatbot.git
cd rag-pdf-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

Download and install Ollama:

https://ollama.com

Pull the Llama 3 model:

```bash
ollama pull llama3
```

Run Ollama:

```bash
ollama serve
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Open browser:

```text
http://localhost:8501
```

---

## 📖 How It Works

1. User uploads a PDF document.
2. Text is extracted from the PDF.
3. Content is split into semantic chunks.
4. Embeddings are generated using Sentence Transformers.
5. Embeddings are stored in a FAISS index.
6. User asks a question.
7. Relevant chunks are retrieved from FAISS.
8. Retrieved context is sent to Llama 3 through Ollama.
9. Answer is generated and displayed.

---

## 🎯 Use Cases

- Academic PDF Question Answering
- Research Paper Analysis
- Document Search
- Knowledge Base Assistant
- Study Material Exploration

---

## 👩‍💻 Author
pragna
