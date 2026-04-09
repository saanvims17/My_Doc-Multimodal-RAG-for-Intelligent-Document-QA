# My_Doc - Multimodal RAG for Intelligent Document QA 
Transform any PDF into a searchable, explainable AI-powered knowledge system. 
MyDOC is an end-to-end Multimodal Retrieval-Augmented Generation (RAG) pipeline that processes documents containing text, tables, and images, enabling accurate, grounded question answering. Powered by GPT-4o and ChromaDB, with full support for text, tables, and embedded images.

**Pipeline Architecture** 
PDF → Partition → Chunk → Summarize → Embed → Store → Retrieve → Answer → Evaluate

<img width="1042" height="478" alt="Screenshot 2026-04-09 at 7 06 13 PM" src="https://github.com/user-attachments/assets/bae08c34-c296-4f5b-a0e6-839bb5848a74" />

**Ingestion Pipeline** 

<img width="595" height="494" alt="Screenshot 2026-04-09 at 7 15 50 AM" src="https://github.com/user-attachments/assets/aae0e928-0024-4e11-b9ef-94af70ca3f51" />

<img width="1246" height="472" alt="Screenshot 2026-04-09 at 7 36 49 PM" src="https://github.com/user-attachments/assets/f4186437-4212-440c-957e-df2ca6cbb3f4" />


### Features

- Multimodal extraction — pulls text, HTML tables, and base64-encoded images from PDFs using Unstructured's high-resolution strategy

- Smart chunking — title-aware chunking keeps semantically related content together

- AI-enhanced summaries — GPT-4o writes searchable descriptions for chunks containing tables or images; raw text is always preserved for faithful answer generation

- Dual-index design — embeddings are built from AI summaries (richer retrieval signal); the LLM answers from original raw text (no information loss)

- MMR retrieval — Maximal Marginal Relevance prevents duplicate chunks from dominating results

- Chat UI — a clean, persistent conversation interface built with Streamlit

- Source transparency — every answer exposes the source chunks it was grounded in, tagged by type (text / table / image)

### Project Structure

.
  ├── mydoc_rag_pipeline.py      # Core RAG pipeline (partition → chunk → embed → retrieve → answer)

  ├── app.py             # Streamlit chat interface

  └── README.md

  └── .env 

  --- 
  ### Requirements - 
Python packages 

unstructured[pdf]

langchain-core

langchain-openai

langchain-chroma

openai

streamlit

python-dotenv

### Install everything 

pip install "unstructured[pdf]" langchain-core langchain-openai langchain-chroma openai streamlit python-dotenv

--- 
###  System-level dependencies

### macOS
brew install poppler tesseract

### Ubuntu 
apt-get install -y poppler-utils tesseract-ocr

--- 

### Environment variables

Create a .env file in the project root:

OPENAI_API_KEY=sk-...

--- 
### Quickstart - Run the Streamlit app

streamlit run app.py

Open http://localhost:8501 in your browser, then:

- Upload a PDF in the sidebar

- Click Process Document

- Watch the live log as the pipeline runs — elements extracted, chunks created, embeddings built

- Ask questions in the chat input at the bottom of the page

--- 

### Run the pipeline from the terminal

python my_doc_rag.py

--- 

