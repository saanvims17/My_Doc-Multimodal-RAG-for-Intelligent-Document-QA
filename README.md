# My_Doc - Multimodal RAG for Intelligent Document QA 
Transform any PDF into a searchable, explainable AI-powered knowledge system. 
MyDOC is an end-to-end Multimodal Retrieval-Augmented Generation (RAG) pipeline that processes documents containing text, tables, and images, enabling accurate, grounded question answering. Powered by GPT-4o and ChromaDB, with full support for text, tables, and embedded images. 

**Streamlit Output** 
**Understands complex documents like a research paper**

<img width="1420" height="785" alt="Screenshot 2026-04-09 at 11 45 01 PM" src="https://github.com/user-attachments/assets/e3a0193a-ed13-4cf0-855a-8789540f90e9" />

**Pipeline Architecture** 
PDF → Partition → Chunk → Summarize → Embed → Store → Retrieve → Answer 

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

--- 

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

### Module Reference — my_doc_rag.py

**partition_document(file_path)**

- Extracts all elements from a PDF using Unstructured's hi_res strategy. Infers table structure and extracts image blocks as base64 payloads.
  
- Returns a list of Unstructured elements.

**create_chunks_by_title(elements)**

- Groups elements into chunks using title boundaries.

Parameter	Value

max_characters	3 000

new_after_n_chars	2 400

combine_text_under_n_chars	500

Returns a list of chunks.

**separate_content_types(chunk)**

Inspects a chunk's orig_elements and splits content into text, tables (HTML strings), and images (base64 strings).

Returns a dict with keys text, tables, images, and types.

**create_ai_enhanced_summary(text, tables, images)**

Calls GPT-4o to generate a searchable description from a chunk's text and tables. The system prompt instructs the model to preserve all numbers, percentages, model dimensions, and named values exactly as they appear in the source.

Returns a summary string. Falls back to text[:300] on API error.

**summarise_chunks(chunks)**

- Iterates over chunks, calls create_ai_enhanced_summary() for chunks that contain tables or images, and builds LangChain Document objects.

- page_content is set to the AI summary (used for embedding)

- metadata["original_content"] stores the full raw text, table HTML, and image base64 data as a JSON string (used for answering)

- Returns a list of langchain_core.documents.Document.

**create_vector_store(documents)**

- Embeds documents using text-embedding-3-small and stores them in an in-memory ChromaDB instance.

- Returns a Chroma vectorstore.

- retrieve(db, query, k=6)

- Queries the vectorstore using MMR (Maximal Marginal Relevance) with a candidate pool of 20 (fetch_k=20). MMR balances relevance against diversity to prevent the same section from filling all result slots.

- Returns a list of Document objects.

**generate_final_answer(chunks, query)**

Assembles context by reading raw_text from each chunk's metadata (falling back to page_content). Passes the context and query to GPT-4o with a strict instruction to answer only from the provided context.

Returns an answer string.

**run_complete_ingestion_pipeline(pdf_path)**

Convenience wrapper that chains partition_document → create_chunks_by_title → summarise_chunks → create_vector_store and returns a ready-to-query vectorstore. Used by the terminal interface in __main__.

---

### Known Limitations 

- Single document per session — the app is designed for one active PDF at a time. Clicking Clear session resets the vectorstore, chat history, and all session state.

- In-memory vectorstore — create_vector_store() does not persist the ChromaDB index to disk. The index is lost when the Python process exits or when Clear session is clicked. Re-upload the PDF to rebuild it.

