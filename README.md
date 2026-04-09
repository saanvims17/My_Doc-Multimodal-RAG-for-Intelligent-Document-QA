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
Text

Tables (HTML structured)

Images (base64)

**Processing Pipeline**
Chunking → Title-based semantic chunks

Summarization → GPT-4o (for multimodal understanding)

Embedding → OpenAI text-embedding-3-small

**Query Pipeline**
Retrieve top-k relevant chunks (ChromaDB)

Generate grounded answers using GPT-4o

Evaluate using GPT-4o as a judge

**Key Features**

- Extracts structured content from PDFs (text, tables, images)
  
- Creates intelligent chunks using title-based segmentation
  
- Enhances chunks using AI-powered summarization

- Reads Images and tables via summaries to prevent loss of information 
  
- Generates embeddings and stores them in a vector database (ChromaDB)
  
- Retrieves the most relevant context for user queries
  
- Generates grounded answers using GPT-4o
  
- Evaluates answer quality using LLM-as-a-judge

