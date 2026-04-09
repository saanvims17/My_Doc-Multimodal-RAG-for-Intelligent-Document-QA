# My_Doc - Intelligent Multimodal RAG System
Transform any PDF into a searchable, explainable AI-powered knowledge system. 
MyDOC is an end-to-end Multimodal Retrieval-Augmented Generation (RAG) pipeline that processes documents containing text, tables, and images, enabling accurate, grounded question answering with built-in evaluation.

**Pipeline Architecture** 
PDF → Partition → Chunk → Summarize → Embed → Store → Retrieve → Answer → Evaluate

<img width="1042" height="478" alt="Screenshot 2026-04-09 at 7 06 13 PM" src="https://github.com/user-attachments/assets/bae08c34-c296-4f5b-a0e6-839bb5848a74" />

**Ingestion Pipeline** 

<img width="595" height="494" alt="Screenshot 2026-04-09 at 7 15 50 AM" src="https://github.com/user-attachments/assets/aae0e928-0024-4e11-b9ef-94af70ca3f51" />

PDF parsing using Unstructured.io

**Extracts:**

<img width="1246" height="472" alt="Screenshot 2026-04-09 at 7 36 49 PM" src="https://github.com/user-attachments/assets/f4186437-4212-440c-957e-df2ca6cbb3f4" />


### 1. PDF Partitioning
- Uses **Unstructured.io**
- Extracts:
  - Text blocks
  - Tables (structured HTML)
  - Images (base64 encoded)

---

### 2. Intelligent Chunking
- Title-based chunking strategy
- Maintains semantic grouping
- Configurable chunk size limits

---

### 3. Content Separation
Each chunk is analyzed and split into:
- Text
- Tables
- Images

---

### 4. AI-Enhanced Summarization
- Applied only when tables/images exist
- Uses **GPT-4o**
- Produces searchable descriptions for better retrieval

---

### 5. Vector Store (ChromaDB)
- Embeddings: `text-embedding-3-small`
- Stored in **Chroma vector database**

---

### 6. Retrieval
- Top-k semantic retrieval
- Uses LangChain retriever interface

---

### 7. Answer Generation
- Uses **GPT-4o**
- Receives:
  - Raw text
  - Tables (HTML)
  - Images (base64)

✔ Strict grounding:
- Answers only from retrieved context  
- Explicitly states if information is missing  

---

### 8. Evaluation (LLM-as-a-Judge)

#### Retrieval Evaluation
- Contains answer
- Relevance score
- Coverage score
- Noise score

#### Answer Evaluation
- Faithfulness
- Correctness
- Completeness
- Hallucination detection

---

**Tech Stack**

- LangChain
  
- ChromaDB (Vector Store)
  
- OpenAI GPT-4o
  
- Unstructured.io (PDF parsing)
  
- Python

**Installations** 

pip install \

unstructured[all-docs] \

langchain \

langchain-community \

langchain-openai \

langchain-chroma \

python-dotenv 

**system dependencies** 

**1. Poppler (`poppler-utils`)**
   
- Enables PDF parsing and layout extraction
  
- Required for high-resolution document processing  

**2. Tesseract (`tesseract-ocr`)**
   
- Performs OCR (Optical Character Recognition)
  
- Extracts text from scanned documents and images  

**3. libmagic**
   
- Detects file types based on content
   
- Ensures correct parsing strategy  


**for Mac**: brew install poppler tesseract libmagic

**for Linux**: apt-get install poppler-utils tesseract-ocr libmagic-dev

**RUN the notebook**

python my_doc.ipynb 

**Key Features** 


